from encrypt.doccrypt import bcrypt
from flask import Flask, jsonify, request, Blueprint
from database.db import conexion

update = Blueprint('update', __name__, url_prefix='/api/update/')

# Activar un usuario
@update.put('activate/user/<u_id>')
def activar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_activate_user', [
            u_id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario activado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Desactivar un usaurio
@update.put('deactivate/user/<u_id>')
def desactivar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_deactivate_user', [
            u_id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario desactivado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@update.put('menu/<id>')
def actualizar_menu(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_menu', [
            id,
            request.json['m_title'],
            request.json['m_url'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('instituto/<id>')
def actualizar_intituto(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_institute', [
            id,
            request.json['mi_institute'],
            request.json['mi_address'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500

@update.put('especialidad/<id>')
def actualizar_especialidad(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_speciality', [
            id,
            request.json['s_name'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Especialidad actualizada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('user')
def actualizar_usuario():
    try:
        cursor = conexion.connection.cursor()
        # "u_password" in request.json
        if request.json['u_password'] == "":
            cursor.callproc('sp_update_user_pass_no_change', [
                request.json['u_email'],
                request.json['u_name'],
                request.json['u_last_name'],
                request.json['u_last_m_name'],
                request.json['u_phone'],
                request.json['u_status_p'],
                request.json['u_r_id'],
                request.json['u_s_id'],
                request.json['u_id'],
            ])
        else:
            cursor.callproc('sp_update_user', [
                request.json['u_email'],
                request.json['u_name'],
                request.json['u_last_name'],
                request.json['u_last_m_name'],
                bcrypt.generate_password_hash(request.json['u_password']),
                request.json['u_phone'],
                request.json['u_status_p'],
                request.json['u_r_id'],
                request.json['u_s_id'],
                request.json['u_id'],
            ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario actualizado.'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('rol/<id>')
def actualizar_rol(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_role', [
            id,
            request.json['r_name'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Rol actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('rol/menu/<menu_id>')
def actualizar_rol_menu(menu_id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_rol_menu', [
            menu_id, # menu
            request.json['rmr_r_id'], # rol
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Rol actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500

@update.put('estudios/medicos/<id>')
def actualizar_estudios_medicos(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_study_medical', [
            id,
            request.json['ma_date_study'],
            request.json['ma_description'],
            request.json['ma_mi_id'], # instituto 
            request.json['ma_cs_id'], # categoria
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('categoria/estudios/<id>')
def actualizar_categoria_estudios(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_category_study', [
            id,
            request.json['cs_name'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Categoria actualizada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('dicom/<id>')
def actualizar_dicom(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_dicom', [
            id,
            request.json['d_serie'],
            request.json['d_dicom'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Dicom actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('imagen/<id>')
def actualizar_imagen(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_image', [
            id,
            request.json['i_d_serie'],
            request.json['i_image'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        
        return jsonify({'mensaje':'Imagen actualizada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500
    
@update.put('historial/medico/<id_usuario>')
def actualizar_historial_medico(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_update_medical_history', [
            id_usuario,
            request.json['hm_ma_id'],
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Historial actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'}),500