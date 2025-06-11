from flask import Flask, render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form.get('name')  # Cambiado a 'name'
        email = request.form.get('email')
        mensaje = request.form.get('message')  # Cambiado a 'message'
        # Puedes procesar los datos aquí (guardar en BD, enviar email, etc.)
        return render_template('contact_enviado.html', nombre=nombre, email=email, mensaje=mensaje)
    return render_template('contact.html')

@app.route('/contact_enviado')
def contact_enviado():
    # Ejemplo de datos simulados para mostrar en la página si se accede desde el menú
    nombre = 'Ejemplo Nombre'
    email = 'ejemplo@email.com'
    mensaje = 'Este es un mensaje de ejemplo.'
    return render_template('contact_enviado.html', nombre=nombre, email=email, mensaje=mensaje)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        data = request.json # Datos JSON
        file = request.files.get('file') # Archivo subido
        param = request.args.get('param') # Query string
        # Procesar los datos recibidos
        return render_template('contact_enviado.html', data=data, file=file, param=param)

# Elimina o comenta la línea incorrecta:
# @app.render._template('contact_enviado.html')  
 
# Renderizar la plantilla contact_enviado.html
# con los datos recibidos
def run():
    app.run(debug=True)