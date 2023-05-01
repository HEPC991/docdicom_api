from flask import Flask, jsonify, request, Blueprint
from database.db import conexion
from encrypt.doccrypt import bcrypt

validate = Blueprint('validate', __name__, url_prefix='/api/validate/')

# Validacion del usuario
@validate.post('user')
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