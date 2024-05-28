from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde el archivo config.py
app.config.from_pyfile('config.py')

# Configurar la base de datos SQLAlchemy
db = SQLAlchemy(app)

# Importar las rutas después de crear la aplicación para evitar ciclos de importación
from app import routes
