from flask import Flask, jsonify, request, Blueprint, send_file, Response
import pydicom
from PIL import Image
from io import BytesIO
from database.db import conexion
import base64
import numpy as np
import cv2
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
    

# Listar los estudio medicos
@select.get('medic_study/all')
def get_estudios():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_medic_study')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'Estudios':datos})
    except Exception as ex:
        return jsonify({'mensaje':ex})
    
# Listar todos los institutos medicos
@select.get('institute/all')
def get_institutos():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_institute')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'Institutos':datos})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})
    
# Obtener los menus del sistema del dashboard
@select.get('menus/all')
def get_menus():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('sp_get_menus')
        datos = cursor.fetchall()
        return jsonify({'mensaje':'estudios listados.', 'menus':datos})
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
