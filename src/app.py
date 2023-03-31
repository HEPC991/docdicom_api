from flask import Flask,jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion =MySQL(app)

@app.route('/api/get/usuarios/all', methods = ['GET'])

def get_usuarios():
    try:
        cursor= conexion.connection.cursor()
        sql = "Select u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status, u_s_id, u_r_id FROM users"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'u_email':fila[0], 'u_name':fila[1], 'u_last_name':fila[2], 
                     'u_last_m_name':fila[3], 'u_password':fila[4], 'u_phone':fila[5], 'u_status':fila[6],
                       'u_s_id':fila[7], 'u_r_id':fila[8]}
            usuarios.append(curso)
        return jsonify({'usuarios':usuarios, 'mensaje':'usuarios listados.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})

@app.route('/api/register/<paciente>', methods = ['POST'])
def registrar_usuario(paciente):
    try:
        cursor = conexion.connection.cursor()
        if paciente == 10000001:
            sql = "CALL insert_patient('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone']
            )
        
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

@app.route('/cursos/<idusr>',methods=['PUT'])
def activar_usuario(idusr):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE curso SET nombre = '{0}', creditos = {1} WHERE codigo = '{2}'".format(request.json['nombre'], request.json['creditos'],codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario actualizado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()