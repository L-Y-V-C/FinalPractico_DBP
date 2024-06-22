from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
from models.MUsuario import MUsuario
from models.entidades.usuario import usuario
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync
from ariadne.asgi import GraphQL
from resolvers import query, mutation
import os

app= Flask(__name__)
conexion=MySQL(app)
login_man=LoginManager(app)

#SCHEMA
#-------------SE DEBE CAMBIAR LA RUTA PARA QUE FUNCIONE-----------
type_defs = load_schema_from_path("C:\\Users\\tanuki\\Documents\\ucsp\\DBP\\FinalPractico")
#-----------------------------------------------------------------
schema = make_executable_schema(type_defs, query,mutation)
app_GRAPHQL = GraphQL(schema, debug=True)

#GRAPHQL
def get_all_publicaciones():
    query_string = '{ all_publicaciones { id nombre_publicacion descripcion ruta_imagen } }'
    success, result = graphql_sync(schema, {'query': query_string})
    if success:
        return result['data']['all_publicaciones']
    else:
        print(f"Error fetching PUBLICACIONES(MAIN): {result}")
        return []

def get_all_users():
    query_string = '{ all_users { id username password nom_comple estado rol } }'
    success, result = graphql_sync(schema, {'query': query_string})
    if success:
        return result['data']['all_users']
    else:
        print(f"Error fetching Users(MAIN): {result}")
        return []

def user_by_id(id):
    query_string = f'{{ user_by_id(id: {id}) {{ id username password nom_comple estado rol }} }}'
    success, result = graphql_sync(schema, {'query': query_string})
    if success:
        data = result['data']['user_by_id']
        return usuario(data['id'], data['username'], data['password'], data['nom_comple'], data['estado'], data['rol'])
    else:
        print(f"Error fetching Users(MAIN): {result}")
        return []

@login_man.user_loader
def load(id):
    user = user_by_id(id)
    if user:
        print("Rol del usuario cargado:", user.rol)
    else:
        print("Usuario no encontrado")
    return user

base_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(base_dir, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return redirect(url_for('listaMenu'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=usuario(0,request.form['username'],request.form['password'])
        logged=MUsuario.login(conexion,user)
        if(logged != None):
            if(logged.password):
                login_user(logged)
                return redirect(url_for('listaMenu'))
            else:
                flash("Contraseña invalida..")
                return render_template('index.html')
        else:
            flash("No encontrado el usuario..")
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')

@app.route('/registro')
def reg():
    return render_template('registro.html')

@app.route('/crear-reg',methods=['GET','POST'])
def crear_reg():
    username = request.form['username']
    password = request.form['password']
    nom_comple = request.form['nom_comple']
    mutation_string = '''
    mutation {
        crear_reg(username: "%s", password: "%s", nom_comple: "%s") {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    ''' % (username, password, nom_comple)
    success, result = graphql_sync(schema, {'query': mutation_string})
    if success:
        return render_template('index.html')
    else:
        flash(f"No se pudo crear el usuario: {result}")
        return render_template('registro.html')

@app.route('/formulario', methods=['GET', 'POST'])
@login_required
def formulario():
    if request.method == 'POST':
        alias = request.form['alias']
        descripcion = request.form['descripcion']
        archivo = request.files['archivo']
        archivo_nombre = archivo.filename
        archivo_guardado = os.path.join(app.config['UPLOAD_FOLDER'], archivo_nombre)
        archivo.save(archivo_guardado)
        mutation_string = '''
        mutation {
            crear_pub(nombre_publicacion: "%s", descripcion: "%s", ruta_imagen: "%s") {
                id
                nombre_publicacion
                descripcion
                ruta_imagen
            }
        }
        ''' % (alias, descripcion, archivo_nombre)
        success, result = graphql_sync(schema, {'query': mutation_string})
        if success:
            publicacion_data = result['data']['crear_pub']
            return render_template('form_datos.html', alias=publicacion_data['nombre_publicacion'], descripcion=publicacion_data['descripcion'], archivo_nombre=publicacion_data['ruta_imagen'])
        else:
            flash(f"No se pudo crear la publicación: {result}")
            return render_template('form_file.html')
    return render_template('form_file.html')

#USUARIOS
@app.route('/listarUsuarios', methods=['GET','POST'])
@login_required
def listarUsuarios():
    usuarios = get_all_users()
    return render_template('admiListaUsuarios.html', usuarios=usuarios)
@app.route('/listarUsuariosOrdUsuAsc', methods=['GET', 'POST'])
@login_required
def listar_usuarios_ord_usu_asc():
    query = """
    query {
        listarUsuariosOrdUsuAsc {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    """
    success, result = graphql_sync(schema, {'query': query})
    if success:
        usuarios1 = result['data']['listarUsuariosOrdUsuAsc']
        return render_template('admiListaUsuarios.html', usuarios=usuarios1)
    else:
        flash(f"No se pudo crear la publicación: {result}")
        return render_template('admiListaUsuarios.html', usuarios=[])

@app.route('/listarUsuariosOrdUsuDesc', methods=['GET','POST'])
@login_required
def listar_usuarios_ord_usu_desc():
    query = """
    query {
        listarUsuariosOrdUsuDesc {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    """
    success, result = graphql_sync(schema, {'query': query})
    if success:
        usuarios1 = result['data']['listarUsuariosOrdUsuDesc']
        return render_template('admiListaUsuarios.html', usuarios=usuarios1)
    else:
        flash(f"No se pudo crear la publicación: {result}")
        return render_template('admiListaUsuarios.html', usuarios=[])

@app.route('/listarUsuariosOrdNomAsc', methods=['GET','POST'])
@login_required
def listar_usuarios_ord_nom_asc():
    query = """
    query {
        listarUsuariosOrdNomAsc {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    """
    success, result = graphql_sync(schema, {'query': query})
    if success:
        usuarios1 = result['data']['listarUsuariosOrdNomAsc']
        return render_template('admiListaUsuarios.html', usuarios=usuarios1)
    else:
        flash(f"No se pudo crear la publicación: {result}")
        return render_template('admiListaUsuarios.html', usuarios=[])

@app.route('/listarUsuariosOrdNomDesc', methods=['GET','POST'])
@login_required
def listar_usuarios_ord_nom_desc():
    query = """
    query {
        listarUsuariosOrdNomDesc {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    """
    success, result = graphql_sync(schema, {'query': query})
    if success:
        usuarios1 = result['data']['listarUsuariosOrdNomDesc']
        return render_template('admiListaUsuarios.html', usuarios=usuarios1)
    else:
        flash(f"No se pudo crear la publicación: {result}")
        return render_template('admiListaUsuarios.html', usuarios=[])

@app.route('/eliminarUsuario/<id>', methods=['GET','POST'])
@login_required
def eliminarUsuario(id):
    mutation_string = '''
    mutation {{
        delete_user(id: "{}") {{
            id
        }}
    }}
    '''.format(id)
    success, result = graphql_sync(schema, {'query': mutation_string})
    if success:
        return redirect(url_for('listarUsuarios'))
    else:
        flash(f"No se pudo eliminar el usuario: {result}")
        return redirect(url_for('listarUsuarios'))

@app.route('/editarUsuario/<id>')
@login_required
def obtenerUsuario(id):
    usuario = user_by_id(id)
    return render_template('admiEditarUsuario.html', usuario=usuario)

@app.route('/actualizarUsuario/<id>', methods=['POST'])
@login_required
def actualizarUsuario(id):
    username = request.form['username']
    password = request.form['password']
    nom_comple = request.form['nom_comple']
    estado = request.form['estado']
    rol = request.form['rol']
    mutation_string = '''
    mutation {
        edit_user(id: %s, username: "%s", password: "%s", nom_comple: "%s", estado: %s, rol: %s) {
            id
            username
            password
            nom_comple
            estado
            rol
        }
    }
    ''' % (id, username, password, nom_comple, estado, rol)
    success, result = graphql_sync(schema, {'query': mutation_string})
    if success:
        return redirect(url_for('listarUsuarios'))
    else:
        flash(f"No se pudo crear el usuario: {result}")
        return redirect(url_for('listarUsuarios'))

#PUBLICACIONES
@app.route('/listarPublicaciones', methods=['GET','POST'])
@login_required
def listarPublicaciones():
    publicaciones = get_all_publicaciones()
    return render_template('admiListaPublicaciones.html', publicaciones = publicaciones)

@app.route('/eliminarPublicacion/<id>')
@login_required
def eliminarPublicacion(id):
    mutation_string = '''
    mutation {{
        delete_pub(id: "{}") {{
            id
        }}
    }}
    '''.format(id)
    success, result = graphql_sync(schema, {'query': mutation_string})
    if success:
        return redirect(url_for('listarPublicaciones'))
    else:
        flash(f"No se pudo eliminar el usuario: {result}")
        return redirect(url_for('listarPublicaciones'))

@app.route('/listaMenu', methods=['GET','POST'])
@login_required
def listaMenu():
    publicaciones = get_all_publicaciones()
    return render_template('listaMenu.html', publicaciones=publicaciones)

#GESTION DE ERRORES
@app.errorhandler(401)
def acceso_denegado(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def pag_no_encontrada(error):
    return render_template("404.html")

if __name__ == '__main__':
    app.config.from_object(config['develo'])
    app.run()