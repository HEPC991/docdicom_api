from flask import jsonify, Blueprint, Response
from database.db import conexion
import base64
import json

select = Blueprint("select", __name__, url_prefix="/api/get/")

# region listar usuarios
# Listar todos los usarios
@select.get("usuarios/all")
def get_usuarios():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_users")
        datos = cursor.fetchall()
        if datos is not None:
            if len(datos) > 0:
                return (
                    jsonify({"usuarios": datos, "mensaje": "usuarios listados."}),
                    200,
                )
            else:
                return jsonify({"mensaje": "No hay usuarios registrados."}), 404
        else:
            return jsonify({"mensaje": "No hay usuarios registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error de la peticion."}), 500


# Listar todos los usuarios por el id de su rol
@select.get("usuarios/all/by/role/<int:id_rol>")
def obtener_usuarios_por_rol(id_rol):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_users_by_role", [id_rol])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "Usuarios listados.", "Usuarios": datos}), 200
        return jsonify({"mensaje": "No hay usuarios registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error de la peticion."}), 500


# endregion

# region listar estudios medicos
# Listar los estudio medicos
@select.get("medic_study/all")
def get_estudios():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_medic_study")
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "estudios listados.", "Estudios": datos})
        return jsonify({"mensaje": "No hay estudios registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex})


# Listar los estudio medicos por usuario
@select.get("medic_study/all/by/user/<int:id_user>")
def obtner_estudios_por_usuario(id_user):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_medic_study_by_user", [id_user])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "estudios listados.", "Estudios": datos})
        return jsonify({"mensaje": "No hay estudios registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex})


# Listar los estudio medicos por instituto medico
@select.get("medic_study/all/by/institute/<int:id_institute>")
def obtner_estudios_por_institute(id_institute):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_medic_study_by_institute", [id_institute])
        datos = cursor.fetchall()
        if datos is not None and len(datos) > 0:
            return jsonify({"mensaje": "estudios listados.", "Estudios": datos})
        return jsonify({"mensaje": "No hay estudios registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex})


# endregion

# region Listar institutos medicos
# Listar todos los institutos medicos
@select.get("institute/all")
def get_institutos():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_institute")
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "estudios listados.", "Institutos": datos})
        return jsonify({"mensaje": "No hay institutos registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error."})


# Obtener instituto por id
@select.get("institute/<int:id_institute>")
def obtener_institutos_por_id(id_institute):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_institute_by_id", [id_institute])
        institute = cursor.fetchone()
        if institute is not None:
            return jsonify({"mensaje": "estudios listados.", "Instituto": institute})
        return jsonify({"mensaje": "No se han encontrado instituos"}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error."})
# endregion

# region listar los menus del sistema
# Obtener los menus del sistema del dashboard
@select.get("menus/all")
def get_menus():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_menus")
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "estudios listados.", "menus": datos})
        return jsonify({"mensaje": "No hay menus registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error."})

# obtener solo los menus del dashboard por rol
@select.get("menus/<int:id_role>")
def obtener_menus_por_role(id_role):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_menus_by_role", [id_role])
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "menus listados.", "menus": datos})
        return jsonify({"mensaje": "No hay menus registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": "Error."})
# endregion

# region obtner las imagenes transformadas de dicom a png
# obtener imagen usando el id del dicom
@select.get("image/<int:id_dicom>")
def obtener_una_imagen_por_id(id_dicom):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_image", [id_dicom])
        datos = cursor.fetchone()
        imagen = datos["i_image"]
        imagen = base64.b64decode(imagen)
        response = Response(imagen, mimetype="image/png")
        serie = datos["i_d_serie"]
        response.headers.set(
            "Content-Disposition", "attachment", filename=serie + ".png"
        )
        return response
    except Exception as ex:
        return jsonify({"mensaje": ex}), 500

# Obtener todas las imagenes transformadas de dicom a png a partir de su numero de serie
@select.get("images/<string:serie>")
def obtener_imagenes_por_serie(serie):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_images", [serie])
        datos = cursor.fetchall()
        imagenes = []
        for dato in datos:
            imagen = dato["i_image"]
            imagen = base64.b64decode(imagen)
            imagen = base64.b64encode(imagen).decode("utf-8")
            imagenes.append({"imagen": imagen})

        return json.dumps(imagenes)
    except Exception as ex:
        return jsonify({"mensaje": ex}), 500
    
# Obtener todas las imagenes transformadas de dicom a png a partir de su numero de estudio
@select.get("images/<int:no_study>")
def obtener_imagenes_por_estudio_medico(no_study):
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_images_by_study_number", [no_study])
        datos = cursor.fetchall()
        imagenes = []
        for dato in datos:
            imagen_id = dato["i_id"]
            imagen_serie = dato["i_serie"]
            imagen = dato["i_image"]
            imagen = base64.b64decode(imagen)
            imagen = base64.b64encode(imagen).decode("utf-8")
            imagenes.append({"id": imagen_id,"serie": imagen_serie,"imagen": imagen})

        return json.dumps(imagenes)
    except Exception as ex:
        return jsonify({"mensaje": ex}), 500

# obetener todas las imagenes sin distincion
@select.get("image/all")
def obtener_todas_las_imagenes():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_all_images")
        datos = cursor.fetchall()
        imagenes = []
        for dato in datos:
            imagen_id = dato["i_id"]
            imagen_serie = dato["i_serie"]
            imagen_ma_id = dato['medical_appoiment_id']
            imagen = dato["i_image"]
            imagen = base64.b64decode(imagen)
            imagen = base64.b64encode(imagen).decode("utf-8")
            imagenes.append({"id": imagen_id,"serie": imagen_serie,"medical_appoiment_id":imagen_ma_id,"imagen": imagen})

        return json.dumps(imagenes)
    except Exception as ex:
        return jsonify({"mensaje": ex}), 500

# endregion

# region obtener todas las categorias, especialidades y roles
# obtener las categorias
@select.get("categorias/all")
def obtener_todas_categorias():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_categories")
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify({"mensaje": "categorias listadas.", "Categorias": datos})
        return jsonify({"mensaje": "No hay categorias registradas."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex})

# obtener las especialidades
@select.get("especialidades/all")
def obtener_todas_especialidades():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_specialities")
        datos = cursor.fetchall()
        if datos is not None:
            return jsonify(
                {"mensaje": "especialidades listadas.", "Especialidades": datos}
            )
        return jsonify({"mensaje": "No hay especialidades registradas."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex})

# obtener los roles
@select.get("roles/all")
def obtener_todos_roles():
    try:
        cursor = conexion.connection.cursor()
        cursor.callproc("sp_get_roles")
        roles = cursor.fetchall()
        if roles is not None:
            return jsonify({"message": "Roles listados", "roles": roles})
        return jsonify({"message": "No hay roles registrados."}), 404
    except Exception as ex:
        return jsonify({"mensaje": ex}), 500

# endregion