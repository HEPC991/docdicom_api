from flask import Flask, jsonify, request, Blueprint, send_file, Response
import pydicom
from PIL import Image
from io import BytesIO
from database.db import conexion
import base64
import numpy as np
import json

select = Blueprint('select', __name__, url_prefix='/api/get/')

# Listar todos los usarios
@select.get('usuarios/all')
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
    
@select.get('usuarios/all/by/role/<int:id_rol>')
def obtener_usuarios_por_rol(id_rol):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_get_users_by_role', [id_rol])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'Administradores listados.', 'Administradores':datos}), 200
        return jsonify({'mensaje':'No hay administradores registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error de la peticion.'}), 500


# Listar los estudio medicos
@select.get('medic_study/all')
def get_estudios():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_study')
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'estudios listados.', 'Estudios':datos})
        return jsonify({'mensaje':'No hay estudios registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
# Listar los estudio medicos por usuario
@select.get('medic_study/all/by/user/<int:id_user>')
def obtner_estudios_por_usuario(id_user):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_study_by_user', [id_user])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'estudios listados.', 'Estudios':datos})
        return jsonify({'mensaje':'No hay estudios registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
# Listar los estudio medicos por instituto medico
@select.get('medic_study/all/by/user/<int:id_institute>')
def obtner_estudios_por_institute(id_institute):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_study_by_institute', [id_institute])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'estudios listados.', 'Estudios':datos})
        return jsonify({'mensaje':'No hay estudios registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
# Listar todos los institutos medicos
@select.get('institute/all')
def get_institutos():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_institute')
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'estudios listados.', 'Institutos':datos})
        return jsonify({'mensaje':'No hay institutos registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
    
# Listar todos los institutos medicos
@select.get('institute/<int:id_institute>')
def get_institutos(id_institute):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_institute', [id_institute])
        institute = cursor.fetchone()
        if institute is not None:
            return jsonify({'mensaje':'estudios listados.', 'Instituto':institute})
        return jsonify({'mensaje':'No se han encontrado instituos'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
    
# Obtener los menus del sistema del dashboard
@select.get('menus/all')
def get_menus():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_menus')
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'estudios listados.', 'menus':datos})
        return jsonify({'mensaje':'No hay menus registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
    
@select.get('menus/<int:id_role>')
def obtener_menus_por_role(id_role):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_menus_by_role', [id_role])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'menus listados.', 'menus':datos})
        return jsonify({'mensaje':'No hay menus registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
    
@select.get('image/<int:id_dicom>')
def obtener_una_imagen_por_id(id_dicom):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_image', [id_dicom])
        datos = cursor.fetchone()
        imagen = datos['i_image']
        imagen = base64.b64decode(imagen)
        response = Response(imagen, mimetype='image/png')
        serie = datos['i_d_serie']
        response.headers.set('Content-Disposition', 'attachment', filename=serie+'.png')
        return response
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500
    

@select.get('images/<string:serie>')
def obtner_imagenes_por_serie(serie):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_images', [serie])
        datos = cursor.fetchall()
        imagenes = []
        for dato in datos:
            imagen = dato['i_image']
            imagen = base64.b64decode(imagen)
            imagen = base64.b64encode(imagen).decode('utf-8')
            imagenes.append({'imagen':imagen})

        return json.dumps(imagenes)
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500
    
@select.get('historial/medico/<int:id_user>')
def obtner_historial_medico_por_usuario(id_user):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_history', [id_user])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'historial listado.', 'Historial':datos})
        return jsonify({'mensaje':'No hay historial registrado.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
@select.get('historial/por/cita/<int:id_cita>')
def obtener_historial_por_cita(id_cita):
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_history_by_cita', [id_cita])
        datos = cursor.fetchone()
        if datos is not None:
            return jsonify({'mensaje':'historial listado.', 'Historial':datos})
        return jsonify({'mensaje':'No hay historial registrado.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
@select.get('categorias/all')
def obtner_todas_categorias():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_categories')
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'categorias listadas.', 'Categorias':datos})
        return jsonify({'mensaje':'No hay categorias registradas.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
@select.get('especialidades/all')
def obtener_todas_especialidades():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_specialities')
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({'mensaje':'especialidades listadas.', 'Especialidades':datos})
        return jsonify({'mensaje':'No hay especialidades registradas.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex})

@select.get('roles/all')
def obtener_todos_roles():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_roles')
        roles = cursor.fetchall()
        if roles is not None:
            return jsonify({'message': 'Roles listados', 'roles': roles})
        return jsonify({'message': 'No hay roles registrados.'}), 404
    except Exception as ex:
        return jsonify({'mensaje':ex}), 500
