import io
from flask import Flask,jsonify, request, send_file
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

@app.route('/api/register/medic_study', methods = ['POST'])
def registrar_estudio():
    try:
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO medical_appoiment (ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
            request.json['ma_date_study'], request.json['ma_description'], request.json['ma_status'], request.json['ma_mi_id'], request.json['ma_cs_id'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

@app.route('/api/validate/user', methods=['POST'])
def validar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('validate_login', [request.json['u_email']])
        fila = cursor.fetchone()
        if fila is not None:
            usuario = {
                'u_email': fila[0],
                'u_password': fila[1],
            }
            return jsonify({'mensaje': 'Usuario validado.', 'usuario': usuario})
        else:
            return jsonify({'mensaje': 'El usuario no existe.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al validar el usuario: {}'.format(str(ex))})      

@app.route('/api/register/<paciente>', methods = ['POST'])
def registrar_usuario(paciente):
    try:
        cursor = conexion.connection.cursor()
        if paciente == 10000000:
            sql = "INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status, u_s_id, u_r_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone'],
                request.json['u_status'], request.json['u_s_id'], request.json['u_r_id']
            )
        elif paciente == 10000001:
            sql = "INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status, u_s_id, u_r_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone'],
                request.json['u_status'], request.json['u_s_id'], request.json['u_r_id']
            )
        elif paciente == 10000002:
            sql = "CALL insert_patient('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone']
            )
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

@app.route('/api/activate/<u_id>',methods=['PUT'])
def activar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE users SET u_status = '{0}' WHERE u_id = '{1}'".format(request.json['u_status'],u_id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario activado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

@app.route('/api/deactivate/<u_id>',methods=['PUT'])
def desactivar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE users SET u_status = '{0}' WHERE u_id = '{1}'".format(request.json['u_status'],u_id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario desactivado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/register/institute', methods = ['POST'])
def registrar_instituto():
    try:
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO medical_institutions (mi_institute, mi_address, mi_status) VALUES ('{0}', '{1}', '{2}')".format(
            request.json['mi_institute'], request.json['mi_address'], request.json['mi_status'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/get/medic_study/all', methods = ['GET'])
def get_estudios():
    try:
        cursor= conexion.connection.cursor()
        sql = "Select ma_date_study, ma_description, ma_status, ma_mi_id, ma_cs_id FROM medical_appoiment"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'ma_date_study':fila[0], 'ma_description':fila[1], 'ma_status':fila[2], 
                     'ma_mi_id':fila[3], 'ma_cs_id':fila[4]}
            usuarios.append(curso)
        return jsonify({'usuarios':usuarios, 'mensaje':'estudios listados.'})
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
@app.route('/api/get/institute/all', methods = ['GET'])
def get_institutos():
    try:
        cursor= conexion.connection.cursor()
        sql = "Select mi_institute, mi_address, mi_status FROM medical_institutions"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'mi_institute':fila[0], 'mi_address':fila[1], 'mi_status':fila[2]}
            usuarios.append(curso)
        return jsonify({'usuarios':usuarios, 'mensaje':'institutos listados.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})

@app.route('/api/get/menus/all', methods = ['GET'])
def get_menus():
    try:
        cursor= conexion.connection.cursor()
        sql = "Select m_title, m_url, m_status FROM menus"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'m_title':fila[0], 'm_url':fila[1], 'm_status':fila[2]}
            usuarios.append(curso)
        return jsonify({'usuarios':usuarios, 'mensaje':'menus listados.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error.'})

@app.route('/api/create/menu', methods = ['POST'])
def crear_menu():
    try:
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO menus (m_title, m_url, m_status) VALUES ('{0}', '{1}', '{2}')".format(
            request.json['m_title'], request.json['m_url'], request.json['m_status'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu registrado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/delete/institute/<id>',methods=['DELETE'])
def eleminar_instituto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM medical_institutions WHERE mi_id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/delete/dicom/<id>',methods=['DELETE'])
def eleminar_dicom(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM dicoms WHERE d_id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Imagen dicom eliminada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/delete/medic_study/<id>',methods=['DELETE'])
def eleminar_estudio(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM medical_appoiment WHERE ma_id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

@app.route('/api/delete/user/<id>',methods=['DELETE'])
def eleminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM users WHERE u_id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
@app.route('/api/delete/menu/<id>',methods=['DELETE'])
def eleminar_menu(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM menus WHERE m_id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()