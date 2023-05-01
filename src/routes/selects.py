from flask import Flask, jsonify, request, Blueprint
from database.db import conexion

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