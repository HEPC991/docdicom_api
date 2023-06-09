from flask import Flask, jsonify, request, Blueprint
from database.db import conexion
from encrypt.doccrypt import bcrypt
import pydicom
from PIL import Image
from io import BytesIO
import base64
import numpy

insert = Blueprint('insert', __name__, url_prefix='/api/register/')

# Optimal register medical study
@insert.post('medical_study')
def register_medical_study():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_register_medic_study', [
            request.json['ms_date_study'], 
            request.json['ms_description'], 
            request.json['ms_mi_id'], 
            request.json['ms_cs_id']])
        # Obtenemos el ultimo id de la tabla medic_study
        ma_id = cursor.fetchone()
        cursor.close()
        conexion.connection.commit()

        return jsonify({
            "message": "register medical study success (pending to upload dicoms)",
            "medical_study_id": ma_id["id"]
        })
        
        # print(request.json)
        # return jsonify({"message": "some"})
    except Exception as ex:
        return jsonify({"message": ex}), 500


# Optimal register medical study dicoms
@insert.post('medical_study_dicom/<int:ma_id>')
def register_md_dicom(ma_id):
    try:        
        dicom = request.files['dicom']
        file = dicom.read()
        dcm = pydicom.dcmread(BytesIO(file)).pixel_array.astype(float)
        dcm_enconded = base64.b64encode(file).decode('utf-8')
        rescaled_img = numpy.maximum(dcm, 0) / dcm.max() * 255
        img = Image.fromarray(numpy.uint8(rescaled_img))

        with BytesIO() as output:
            img.save(output, format="png")
            imagen_codificada = base64.b64encode(output.getvalue()).decode('utf-8')

        cursor = conexion.connection.cursor()
        # serie_number = dcm.SeriesInstanceUID
        serie_number = pydicom.dcmread(BytesIO(file)).SeriesInstanceUID

        cursor.callproc('sp_save_dicom', [
            serie_number,
            dcm_enconded,
            imagen_codificada,
            ma_id
        ])
        
        cursor.close()
        conexion.connection.commit()

        return jsonify({"message": f"Upload dicom success in {ma_id}"}), 201

        # return jsonify({"message": str(type(dicom)), "ma_id": ma_id}), 201
    except Exception as ex:
        return jsonify({"message": ex}), 500


# Registrar un estudio medico
@insert.post('medic_study')
def registrar_estudio():
    try:
        files = request.files.getlist('dicoms')
        body = request.form.to_dict()

        cursor = conexion.connection.cursor()
        cursor.callproc('sp_register_medic_study', [
            body['ms_date_study'], 
            body['ms_description'], 
            body['ms_mi_id'], 
            body['ms_cs_id']])
        # Obtenemos el ultimo id de la tabla medic_study
        # conexion.connection.commit()
        ma_id = cursor.fetchone()
        cursor.close()

        if len(files) > 0:
            for file in files:
                file = file.read()
                dcm = pydicom.dcmread(BytesIO(file))
                dcm_enconded = base64.b64encode(file).decode('utf-8')

                img = Image.fromarray(dcm.pixel_array)
        
                with BytesIO() as output:
                    img.save(output, format="png")
                    imagen_codificada = base64.b64encode(output.getvalue()).decode('utf-8')

                cursor = conexion.connection.cursor()
                serie_number = dcm.SeriesInstanceUID

                cursor.callproc('sp_save_dicom', [
                    serie_number,
                    dcm_enconded,
                    imagen_codificada,
                    ma_id['id']
                ])
                
                conexion.connection.commit()
                cursor.close()

        cursor = conexion.connection.cursor()
        cursor.callproc('sp_register_history', [
            body['u_id'], # id del usuario
            ma_id['id'] # id de la cita medica
        ])
        cursor.connection.commit()
        cursor.close()

        return jsonify({'mensaje':'Estudio registrado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500
    

# Registrar un paciente
@insert.post('<role>')
def registrar_usuario(role):
    try:
        try:
            role = int(role)
        except ValueError as nex:
            return jsonify({'Bad request': 'Bad role'}), 400
        cursor = conexion.connection.cursor()
        # admin and medic
        try:
            flag = True
            cursor.callproc('sp_validate_user', [request.json['u_email']])
            user = cursor.fetchone()
            # close the cursor to execute next query
            cursor.close()
            cursor = conexion.connection.cursor()
            if user is not None:
                flag = False
            if flag:
                if role == 10000000 or role == 10000001:
                    cursor.callproc('sp_create_user',[
                        request.json['u_email'], 
                        request.json['u_name'], 
                        request.json['u_last_name'],
                        request.json['u_last_m_name'], 
                        bcrypt.generate_password_hash(request.json['u_password']), 
                        request.json['u_phone'],
                        request.json['u_status_p'],
                        request.json['u_s_id'],
                        int(role)
                    ])
                elif role == 10000002:
                    cursor.callproc('sp_create_patient', [
                        request.json['u_email'], 
                        request.json['u_name'], 
                        request.json['u_last_name'],
                        request.json['u_last_m_name'], 
                        bcrypt.generate_password_hash(request.json['u_password']), 
                        request.json['u_phone']
                    ])
                else: 
                    return jsonify({'Bad request': 'Role not found'}), 404
            else:
                return jsonify({'Bad request': 'User already exists'}), 400
        except Exception as uex:
            return jsonify({'Bad request': uex}), 400
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario registrado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500
    
# Registrar un instituto medico
@insert.post('institute')
def registrar_instituto():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_register_institute', [
            request.json['mi_name'],
            request.json['mi_address']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
   
# Crear un neuvo menu
@insert.post('menu')
def crear_menu():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_create_menu', [
            request.json['m_title'],
            request.json['m_url'],
            request.json['m_status']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@insert.post('guardar/dicoms/<int:ma_id>')
def guardar_dicoms_y_convertirlos(ma_id):
    try:
        files = request.files.getlist('dicom')

        for file in files:

            file = file.read()
            dcm = pydicom.dcmread(BytesIO(file))
            dcm_enconded = base64.b64encode(file).decode('utf-8')

            img = Image.fromarray(dcm.pixel_array)
    
            with BytesIO() as output:
                img.save(output, format="png")
                imagen_codificada = base64.b64encode(output.getvalue()).decode('utf-8')

            cursor = conexion.connection.cursor()
            serie_number = dcm.SeriesInstanceUID

            cursor.callproc('sp_save_dicom', [
                serie_number,
                dcm_enconded,
                imagen_codificada,
                ma_id
            ])
            

            conexion.connection.commit()
            cursor.close()


        return jsonify({'mensaje':'Dicoms guardados.'})

    except Exception as ex:
        return jsonify({'mensaje':ex})
    