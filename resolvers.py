from ariadne import QueryType, MutationType
from flask import current_app
import MySQLdb

query = QueryType()
mutation = MutationType()

@query.field("all_publicaciones")
def resolve_all_publicaciones(_, info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre_publicacion, descripcion, ruta_imagen FROM publicaciones")
        result = cursor.fetchall()
        publicaciones = []
        for row in result:
            publicacion = {
                "id": row[0],
                "nombre_publicacion": row[1],
                "descripcion": row[2],
                "ruta_imagen": row[3]
            }
            publicaciones.append(publicacion)
        cursor.close()
        return publicaciones
    except Exception as e:
        print(f"No se pudo recolectar las publicaciones (RESOLVER): {e}")
        return []

@query.field("all_users")
def resolve_all_users(_,info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password, nom_comple, estado, rol FROM usuarios")
        result = cursor.fetchall()
        usuarios = []
        for row in result:
            usuario = {
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "nom_comple": row[3],
                "estado": row[4],
                "rol": row[5]
            }
            usuarios.append(usuario)
        cursor.close()
        return usuarios
    except Exception as e:
        print(f"No se pudo recolectar las usuarios (RESOLVER): {e}")
        return []

@query.field("user_by_id")
def resolve_user_by_id(_, info, id):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password, nom_comple, estado, rol FROM usuarios WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result:
            usuario = {
                "id": result[0],
                "username": result[1],
                "password": result[2],
                "nom_comple": result[3],
                "estado": result[4],
                "rol": result[5]
            }
            cursor.close()
            return usuario
        else:
            cursor.close()
            return None
    except Exception as e:
        print(f"No se pudo recolectar el usuario (RESOLVER): {e}")
        return None

@mutation.field("crear_reg")
def resolve_crear_reg(_,info, username, password, nom_comple):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, password, nom_comple, estado, rol) VALUES (%s, %s, %s, '1', '2')",
            (username, password, nom_comple)
        )
        db.commit()

        user_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {
            "id": user_id,
            "username": username,
            "password": password,
            "nom_comple": nom_comple,
            "estado": 1,
            "rol": 2
        }
    except Exception as e:
        print(f"Error creando usuario: {e}")
        return None

@mutation.field("crear_pub")
def resolve_crear_pub(_,info,nombre_publicacion, descripcion, ruta_imagen):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO publicaciones (nombre_publicacion, descripcion, ruta_imagen) VALUES (%s, %s, %s)",
            (nombre_publicacion, descripcion, ruta_imagen)
        )
        db.commit()

        publicacion_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {
            "id": publicacion_id,
            "nombre_publicacion": nombre_publicacion,
            "descripcion": descripcion,
            "ruta_imagen": ruta_imagen
        }
    except Exception as e:
        print(f"Error creando usuario: {e}")
        return None

@mutation.field("edit_user")
def resolve_edit_user(_,info, id, username, password, nom_comple, estado, rol):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute(
            """UPDATE usuarios
            SET username = %s,
            password = %s,
            nom_comple = %s,
            estado = %s,
            rol = %s
            WHERE id = %s""",
            (username, password, nom_comple, estado, rol, id)
        )
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {
            "id": user_id,
            "username": username,
            "password": password,
            "nom_comple": nom_comple,
            "estado": int(estado),
            "rol": int(rol)
        }
    except Exception as e:
        print(f"Error editando usuario: {e}")
        return None

@query.field("listarUsuariosOrdUsuAsc")
def listar_usuarios_ord_usu_asc(_, info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY username ASC")
        db.commit()
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "nom_comple": row[3],
                "estado": row[4],
                "rol": row[5]
            })
        cursor.close()
        db.close()
        return usuarios
    except Exception as ex:
        print(f"Error ordenando usuario: {ex}")
        return None

@query.field("listarUsuariosOrdUsuDesc")
def listar_usuarios_ord_usu_desc(_, info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY username DESC")
        db.commit()
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "nom_comple": row[3],
                "estado": row[4],
                "rol": row[5]
            })
        cursor.close()
        db.close()
        return usuarios
    except Exception as ex:
        print(f"Error ordenando usuario: {ex}")
        return None

@query.field("listarUsuariosOrdNomAsc")
def listar_usuarios_ord_nom_asc(_, info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY nom_comple ASC")
        db.commit()
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "nom_comple": row[3],
                "estado": row[4],
                "rol": row[5]
            })
        cursor.close()
        db.close()
        return usuarios
    except Exception as ex:
        print(f"Error ordenando usuario: {ex}")
        return None

@query.field("listarUsuariosOrdNomDesc")
def listar_usuarios_ord_nom_desc(_, info):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY nom_comple DESC")
        db.commit()
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuarios.append({
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "nom_comple": row[3],
                "estado": row[4],
                "rol": row[5]
            })
        cursor.close()
        db.close()
        return usuarios
    except Exception as ex:
        print(f"Error ordenando usuario: {ex}")
        return None

@mutation.field("delete_user")
def resolve_delete_user(_, info, id):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute(
            """DELETE FROM usuarios WHERE id = %s""",
            (id,)
        )
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {
            "id": id
        }
    except Exception as e:
        print(f"Error eliminando usuario: {e}")
        return None

@mutation.field("delete_pub")
def resolve_delete_user(_, info, id):
    try:
        db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = db.cursor()
        cursor.execute(
            """DELETE FROM publicaciones WHERE id = %s""",
            (id,)
        )
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {
            "id": id
        }
    except Exception as e:
        print(f"Error eliminando Publicacion: {e}")
        return None