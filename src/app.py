import io
from flask import Flask,jsonify, request, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

CORS(app)

conexion =MySQL(app)

# Listar todos los usarios
@app.get('/api/get/usuarios/all')
def get_usuarios():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_users')
        datos = cursor.fetchall()
        if datos is not None:
            if len(datos) > 0:
                return jsonify({'usuarios':datos, 'mensaje':'usuarios listados.'}), 200
            else:
                return jsonify({'mensaje':'No hay usuarios registrados.'}), 404
        else: 
            return jsonify({'mensaje':'No hay usuarios registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error de la peticion.'}), 500


# REgistrar un estudio medico
@app.post('/api/register/medic_study')
def registrar_estudio():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_register_medic_study', [
            request.json['ms_date_study'], 
            request.json['ms_description'], 
            request.json['ms_status'], 
            request.json['ms_mi_id'], 
            request.json['ms_cs_id']])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio registrado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500

# Validacion del usuario
@app.post('/api/validate/user')
def validar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_validate_user', [request.json['u_email']])
        usuario = cursor.fetchone()
        if usuario is not None:
            if bcrypt.check_password_hash(usuario['password'], request.json['u_password']):
                # remove the password field from the json to return it to the client
                del usuario['password']
                return jsonify({'mensaje': 'Usuario validado.', 'usuario': usuario})
            else:
                return jsonify({"mensaje":"Usuario invalido, la contraseña no corresponde."})
        else:
            return jsonify({'mensaje': 'El usuario no existe.'})
    except Exception as ex:
        return jsonify({'Mensaje de error': ex}), 500

@app.get('/api/test/number/<number>')
def test(number):
    try:
        return jsonify({'message': int(number)})
    except ValueError as ex:
        return jsonify({'mensaje':'Error de conversion.'})


# Registrar un paciente
@app.post('/api/register/<role>')
def registrar_usuario(role):
    try:
        try:
            role = int(role)
        except ValueError as nex:
            return jsonify({'Bad request': 'Bad role or activate'}), 400
        cursor = conexion.connection.cursor()
        # admin and medic
        try:
            flag = True
            cursor.callproc('sp_validate_user', [request.json['u_email']])
            user = cursor.fetchone()
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
                    return jsonify({'Bad request': 'Role not found'})
            else:
                return jsonify({'Bad request': 'User already exists'})
        except Exception as uex:
            return jsonify({})
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':ex})

# Activar un usuario
@app.put('/api/activate/<u_id>')
def activar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_activate_user', [u_id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario activado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Desactivar un usaurio
@app.put('/api/deactivate/<u_id>')
def desactivar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_deactivate_user', [u_id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario desactivado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Registrar un instituto medico
@app.post('/api/register/institute')
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
    
# Listar los estudio medicos
@app.get('/api/get/medic_study/all')
def get_estudios():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_study')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'Estudios':datos})
    except Exception as ex:
        return jsonify({'mensaje':ex})
"""   
@app.route('/api/get/dicom/all', methods=['GET'])
def get_dicom():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT d_serie, d_dicom, d_status, d_ma_id FROM dicoms"
        cursor.execute(sql)
        datos = cursor.fetchone()
        
        return send_file(io.BytesIO(datos[1]), attachment_filename='dicom.dcm', as_attachment=True)
    except Exception as ex:
        return jsonify({'mensaje': 'Error.'})
"""
"""
@app.route('/api/get/dicom/all', methods = ['GET'])
def get_dicom():
    try:
        cursor= conexion.connection.cursor()
        sql = "Select d_serie, d_status, d_ma_id, d_dicom FROM dicoms"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'d_serie':fila[0], 'd_status':fila[1], 'd_ma_id':fila[2]}
            usuarios.append(curso)
        return jsonify({'usuarios':usuarios, 'mensaje':'Imagenes DICOM listadas.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
"""

# Listar todos los institutos medicos
@app.get('/api/get/institute/all')
def get_institutos():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_institute')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'Institutos':datos})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})

# Obtener los menus del sistema del dashboard
@app.get('/api/get/menus/all')
def get_menus():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_menus')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'menus':datos})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})

# Crear un neuvo menu
@app.post('/api/create/menu')
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
    
# Eliminar un instituto
@app.delete('/api/delete/institute/<id>')
def eleminar_instituto(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_institute', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    

@app.route('/api/delete/dicom/<id>',methods=['DELETE'])
def eleminar_dicom(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_dicom', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Imagen dicom eliminada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Borrar un estudio medico
@app.delete('/api/delete/medic_study/<id>')
def eleminar_estudio(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_medic_study', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Eliminar un usuario
@app.delete('/api/delete/user/<id>')
def eleminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_user', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Eliminar un menu
@app.delete('/api/delete/menu/<id>')
def eleminar_menu(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_menu', [
            id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu eliminado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.register_error_handler(404, page_not_found)
    app.run()