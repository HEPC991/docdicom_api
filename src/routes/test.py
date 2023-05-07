from flask import jsonify, request, Blueprint
from database.db import conexion
import pydicom
from PIL import Image
from io import BytesIO
import base64


test = Blueprint('test', __name__, url_prefix='/api/test/')

@test.post('insert/files/and/data')
def test_files_data():
    try:
        files = request.files.getlist('files')
        data = request.form.to_dict()
        filenames = []
        if files is not None or len(files) > 0:
            for file in files:
                filenames.append(file.filename)

        return jsonify({'message':"Not found" if len(filenames) == 0 else filenames, "data":"Not found" if len(data) == 0 else data})

    except Exception as ex:
        return jsonify({'message':ex})

@test.get('number/<number>')
def numberTest(number):
    try:
        return jsonify({'message': int(number)})
    except ValueError as ex:
        return jsonify({'mensaje':'Error de conversion.'})
    
@test.get('convert/dicom/image')
def conversion():
    try:
        cursor = conexion.connection.cursor()
        sql = 'select d_serie, d_dicom from dicoms where d_serie = 2'
        cursor.execute(sql)
        datos = cursor.fetchone()
        cursor.close()
        decoded_file = base64.b64decode(datos['d_dicom'])
        dcm = pydicom.dcmread(BytesIO(decoded_file), force=True)
        img = Image.fromarray(dcm.pixel_array)
        #save the image in the images directory
        
        img.save()
        return jsonify({'message':'ok '})
    except Exception as ex:
        return jsonify({'message':ex})


@test.get('insert/dicom')
def agregar_dicom():
    file = open('C:\\Users\\jordi\\Documents\\repos\\docdicom_api\\src\\routes\\image1.dcm', 'rb')
    dcm_data = file.read()
    cursor = conexion.connection.cursor()
    sql = 'insert into dicoms (d_serie, d_dicom, d_ma_id) values (%s, %s, %s)'
    cursor.execute(sql,  ('1', dcm_data, '10000004'))
    cursor.connection.commit()
    cursor.close()
    return jsonify({'message':'ok'})

@test.post('files/upload')
def upload_files():
    input_file = request.files['dicom']
    file = input_file.read()
    enconded_file = base64.b64encode(file).decode('utf-8')
    cursor = conexion.connection.cursor()
    sql = 'insert into dicoms (d_serie, d_dicom, d_ma_id) values (%s, %s, %s)'
    cursor.execute(sql,  ('2', enconded_file, '10000004'))
    cursor.connection.commit()
    cursor.close()
    return jsonify({'message':'ok'}), 201

@test.post('otro/test/mas')
def upload_image():
    input_file = request.files['dicom']
    file = input_file.read()
    dcm = pydicom.dcmread(BytesIO(file), force=True)
    img = Image.fromarray(dcm.pixel_array)
    
    with BytesIO() as output:
        img.save(output, format="png")
        imagen_codificada = base64.b64encode(output.getvalue()).decode('utf-8')

    cursor = conexion.connection.cursor()
    sql = 'insert into images (i_d_serie, i_image, i_d_id) values (%s, %s, %s)'
    cursor.execute(sql,  ('1.3.6.1.4.1.14519.5.2.1.133056779001602774748954083940172404512', imagen_codificada, '10000038'))
    cursor.connection.commit()
    cursor.close()
    return jsonify({'message':'ok'})