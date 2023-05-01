from flask import Flask, jsonify, Blueprint

handler = Blueprint('handler', __name__)

@handler.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'Route not found'}), 404