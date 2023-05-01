from flask import Flask, jsonify, request, Blueprint
from database.db import conexion

delete = Blueprint('delete', __name__, url_prefix='/api/delete/')

# Eliminar un paciente
# @delete.delete('patient/<id>')

# Eliminar un instituto
@delete.delete('institute/<id>')
def eleminar_instituto(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_institute', [
            id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    

@delete.delete('dicom/<id>')
def eleminar_dicom(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_dicom', [
            id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Imagen dicom eliminada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Borrar un estudio medico
@delete.delete('medic_study/<id>')
def eleminar_estudio(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_medic_study', [
            id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Eliminar un usuario
@delete.delete('user/<id>')
def eleminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_user', [
            id,
            request.remote_addr,
            request.json['m_by_user']
        ])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Eliminar un menu
@delete.delete('menu/<id>')
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