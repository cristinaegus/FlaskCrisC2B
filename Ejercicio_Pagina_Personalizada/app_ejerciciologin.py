from flask import Flask, render_template, request, redirect, url_for, session, make_response
# Importar CSRFProtect para proteger contra ataques CSRF
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'tu_clave_secreta_ultrasegura' # Necesaria para CSRF
csrf = CSRFProtect(app)
# Configuración de CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'tu_clave_secreta_csrf'  # Cambia esto por una clave secreta segura

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://FlaskEjercicioConnect_owner:npg_4SBm3VXpFwIE@ep-floral-frost-a2tieivc-pooler.eu-central-1.aws.neon.tech/FlaskEjercicioConnect?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LoginUsuario(db.Model):
    __tablename__ = 'login_usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def configurar():
    color = request.cookies.get('color')
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        color = request.form.get('color')
        # Guardar en la base de datos
        nuevo_usuario = LoginUsuario(nombre=nombre, apellido=apellido, email=email)
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            mensaje = 'Usuario guardado correctamente en la base de datos.'
        except Exception as e:
            db.session.rollback()
            mensaje = 'Error: el email ya está registrado.'
        resp = make_response(redirect(url_for('bienvenida')))
        resp.set_cookie('color', color)
        session['mensaje'] = mensaje
        return resp
    # Si no hay color en la cookie, usar blanco por defecto
    if not color:
        color = '#ffffff'
    mensaje = session.pop('mensaje', None)
    # No rellenar los campos con datos de sesión, siempre vacíos
    return render_template('configurar.html', nombre='', apellido='', email='', color=color, mensaje=mensaje)

@app.route('/bienvenida')
def bienvenida():
    nombre = session.get('nombre')
    color = request.cookies.get('color')
    if not nombre:
        return redirect(url_for('configurar'))
    # Si no hay color en la cookie, usar blanco por defecto
    if not color:
        color = '#ffffff'
    return render_template('inicio.html', nombre=nombre, color=color)

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
