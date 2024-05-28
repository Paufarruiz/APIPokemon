import os

# Obtener la ruta base del directorio del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URI = 'mysql://Pau:Monlau@51.141.92.127/Pokemon'
SQLALCHEMY_TRACK_MODIFICATIONS = False
