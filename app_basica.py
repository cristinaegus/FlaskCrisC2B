# app_basico.py
from flask import Flask, send_from_directory
import os

# Crear aplicación Flask
app = Flask(__name__)

# Ruta básica
@app.route('/')
def hola_mundo():
    return '<h1>¡Hola Mundo desde Flask!</h1>'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
app.secret_key = os.environ.get('SECRET_KEY')
# Configuración de la clave secreta
# Asegúrate de establecer la variable de entorno SECRET_KEY antes de ejecutar la aplicación
print(os.urandom(24).hex())
