from flask import Flask, render_template, request, redirect, url_for, session, make_response
# Importar CSRFProtect para proteger contra ataques CSRF
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
from flask import send_from_directory


app = Flask(__name__)

# Cargar configuración desde instance/config.py (ruta absoluta)
instance_path = os.path.join(os.path.dirname(__file__), 'instance')
app.config.from_pyfile(os.path.join(instance_path, 'config.py'))
app.secret_key = app.config['SECRET_KEY']
csrf = CSRFProtect(app)
# Configuración de CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = app.config['CSRF_SECRET_KEY']

db = SQLAlchemy(app)

class LoginUsuario(db.Model):
    __tablename__ = 'login_usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Tarea:
    def __init__(self, descripcion, estado):
        self.descripcion = descripcion
        self.estado = estado

def get_tareas_usuario():
    return session.get('tareas', [])

def add_tarea_usuario(descripcion, estado):
    tareas = session.get('tareas', [])
    tareas.append({'descripcion': descripcion, 'estado': estado})
    session['tareas'] = tareas

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
@app.route('/', methods=['GET', 'POST'])
def configurar():
    color = request.cookies.get('color')
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        color = request.form.get('color')
        # Verificar si el email ya existe antes de guardar
        existe = LoginUsuario.query.filter_by(email=email).first()
        if existe:
            mensaje = 'Error: el email ya está registrado.'
        else:
            nuevo_usuario = LoginUsuario(nombre=nombre, apellido=apellido, email=email)
            db.session.add(nuevo_usuario)
            try:
                db.session.commit()
                mensaje = 'Usuario guardado correctamente en la base de datos.'
            except Exception as e:
                db.session.rollback()
                mensaje = 'Error al guardar el usuario.'
        resp = make_response(redirect(url_for('bienvenida')))
        resp.set_cookie('color', color)
        session['nombre'] = nombre
        session['mensaje'] = mensaje
        return resp
    # Si no hay color en la cookie, usar blanco por defecto
    if not color:
        color = '#ffffff'
    mensaje = session.pop('mensaje', None)
    # No rellenar los campos con datos de sesión, siempre vacíos
    return render_template('configurar.html', nombre='', apellido='', email='', color=color, mensaje=mensaje)

@app.route('/bienvenida', methods=['GET', 'POST'])
def bienvenida():
    nombre = session.get('nombre')
    color = request.cookies.get('color')
    if not nombre:
        resp = make_response(redirect(url_for('configurar')))
        resp.set_cookie('color', '', expires=0)
        return resp
    if not color:
        color = '#ffffff'
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        estado = request.form.get('estado')
        # Validación: ambos campos deben estar presentes
        if not descripcion or not estado:
            tareas = [Tarea(t['descripcion'], t['estado']) for t in get_tareas_usuario()]
            return render_template('inicio.html', nombre=nombre, color=color, tareas=tareas, mensaje_tarea='Debes completar todos los campos de la tarea.')
        add_tarea_usuario(descripcion, estado)
        return redirect(url_for('bienvenida'))
    tareas = [Tarea(t['descripcion'], t['estado']) for t in get_tareas_usuario()]
    return render_template('inicio.html', nombre=nombre, color=color, tareas=tareas)

@app.route('/olvidar')
def olvidar():
    session.pop('nombre', None)
    resp = make_response(redirect(url_for('configurar')))
    resp.set_cookie('color', '', expires=0)
    return resp

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
