from flask import Flask, jsonify, request, Blueprint
from database.db import conexion

test = Blueprint('test', __name__, url_prefix='/api/test/')

@test.get('number/<number>')
def numberTest(number):
    try:
        return jsonify({'message': int(number)})
    except ValueError as ex:
        return jsonify({'mensaje':'Error de conversion.'})