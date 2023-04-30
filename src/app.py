import io
from flask import Flask,jsonify, request, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config



app = Flask(__name__)

CORS(app)

conexion =MySQL(app)

# Listar todos los usarios
@app.get('/api/get/usuarios/all')
def get_usuarios():
    try:
        cursor= conexion.connection.cursor()
        cursor.callproc('get_all_users')
        datos = cursor.fetchall()
        return jsonify({'usuarios':datos, 'mensaje':'usuarios listados.'}), 200
    except Exception as ex:
        return jsonify({'mensaje':'Error de la peticion.'}), 400

# REgistrar un estudio medico
@app.post('/api/register/medic_study')
def registrar_estudio():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('register_medic_study', [
            request.json['ms_date_study'], 
            request.json['ms_description'], 
            request.json['ms_status'], 
            request.json['ms_mi_id'], 
            request.json['ms_cs_id']])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio registrado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'}), 400

# Validacion del usuario
@app.post('/api/validate/user')
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
            if usuario['u_password'] == request.json['u_password']:
                return jsonify({'mensaje': 'Usuario validado.', 'usuario': usuario['u_email']})
            else:
                return jsonify({"mensaje":"Usuario invalido, la contraseña no corresponde."})
        else:
            return jsonify({'mensaje': 'El usuario no existe.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al validar el usuario: {}'.format(str(ex))})      

# Registrar un paciente
@app.post('/api/register/<paciente>')
def registrar_usuario(paciente):
    try:
        paciente = int(paciente)
        cursor = conexion.connection.cursor()
        if paciente == 10000000:
            sql = "INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status, u_s_id, u_r_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone'],
                request.json['u_status'], request.json['u_s_id'], int(paciente)
            )
        elif paciente == 10000001:
            sql = "INSERT INTO users (u_email, u_name, u_last_name, u_last_m_name, u_password, u_phone, u_status, u_s_id, u_r_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(
                request.json['u_email'], request.json['u_name'], request.json['u_last_name'],
                request.json['u_last_m_name'], request.json['u_password'], request.json['u_phone'],
                request.json['u_status'], request.json['u_s_id'], paciente
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

# Activar un usuario
@app.put('/api/activate/<u_id>')
def activar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE users SET u_status = '{0}' WHERE u_id = '{1}'".format(request.json['u_status'],u_id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario activado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Desactivar un usaurio
@app.put('/api/deactivate/<u_id>')
def desactivar_usuario(u_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE users SET u_status = '{0}' WHERE u_id = '{1}'".format(request.json['u_status'],u_id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario desactivado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Registrar un instituto medico
@app.post('/api/register/institute')
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
    
# Listar los estudio medicos
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

# Listar todos los institutos medicos
@app.get('/api/get/institute/all')
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

# Obtener los menus del sistema del dashboard
@app.get('/api/get/menus/all')
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

# Crear un neuvo menu
@app.post('/api/create/menu')
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
    
# Eliminar un instituto
@app.delete('/api/delete/institute/<id>')
def eleminar_instituto(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_institute', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Instituto eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    

@app.route('/api/delete/dicom/<id>',methods=['DELETE'])
def eleminar_dicom(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_dicom', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Imagen dicom eliminada.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Borrar un estudio medico
@app.delete('/api/delete/medic_study/<id>')
def eleminar_estudio(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_medic_study', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Estudio eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})

# Eliminar un usuario
@app.delete('/api/delete/user/<id>')
def eleminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_user', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Usuario eliminado.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'})
    
# Eliminar un menu
@app.delete('/api/delete/menu/<id>')
def eleminar_menu(id):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc('sp_delete_menu', [id])
        conexion.connection.commit()
        return jsonify({'mensaje':'Menu eliminado.'}), 201
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion.'}), 500

def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()