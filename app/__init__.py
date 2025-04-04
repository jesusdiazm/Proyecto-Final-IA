from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Cargar las variables de entorno desde venv/.env
    load_dotenv(dotenv_path="venv/.env")

    # Crear instancia de Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Registrar el blueprint con las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
