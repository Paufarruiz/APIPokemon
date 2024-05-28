from flask import jsonify
from app import app, db  # Importa la aplicación Flask y la instancia de la base de datos
from sqlalchemy import inspect  # Importa inspect desde SQLAlchemy

# Mostrar datos de conexión al iniciar la API
print(f"Conexión a la base de datos establecida en: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Realizar una consulta de prueba para mostrar el nombre de las tablas
@app.route('/api/nombres_tablas', methods=['GET'])
def obtener_nombres_tablas():
    try:
        # Crea un inspector para la base de datos actual
        inspector = inspect(db.engine)

        # Obtiene los nombres de las tablas presentes en la base de datos
        nombres_tablas = inspector.get_table_names()

        return jsonify({'tablas': nombres_tablas}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import multiprocessing
    workers = multiprocessing.cpu_count() * 2 + 1
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

