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