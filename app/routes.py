from flask import jsonify, request, abort, Response
from app import app, db
import base64
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from collections import Counter
from app.models import Ataque, Pokemon, Usuario, Carta, LiderGimnasio, Medalla, Pokedex, AtaquePokemon, PokemonLider, Tienda
import datetime


# Ruta para obtener todos los ataques
@app.route('/api/ataques', methods=['GET'])
def get_ataques():
    ataques = Ataque.query.all()
    result = [{'id_ataque': a.id_ataque,
               'nombre_ataque': a.nombre_ataque,
               'tipo_ataque': a.tipo_ataque,
               'pp': a.pp,
               'daño': a.daño} for a in ataques]
    return jsonify(result)

# Ruta para obtener un ataque por su ID
@app.route('/api/ataques/<int:ataque_id>', methods=['GET'])
def get_ataque(ataque_id):
    ataque = Ataque.query.get(ataque_id)
    if not ataque:
        abort(404)  # Si no se encuentra el ataque, devolver 404
    result = {
        'id_ataque': ataque.id_ataque,
        'nombre_ataque': ataque.nombre_ataque,
        'tipo_ataque': ataque.tipo_ataque,
        'pp': ataque.pp,
        'daño': ataque.daño
    }
    return jsonify(result)

# Ruta para obtener todas las combinaciones de Ataque_Pokemon
@app.route('/api/ataque_pokemon', methods=['GET'])
def get_ataque_pokemon():
    ataques_pokemon = AtaquePokemon.query.all()
    result = [{'id_pokemon_ataque': ap.id_pokemon_ataque,
               'id_ataque': ap.id_ataque,
               'id_pokemon': ap.id_pokemon} for ap in ataques_pokemon]
    return jsonify(result)

# Ruta para obtener una combinación de Ataque_Pokemon por su ID
@app.route('/api/ataque_pokemon/<int:id_pokemon_ataque>', methods=['GET'])
def get_ataque_pokemon_by_id(id_pokemon_ataque):
    ataque_pokemon = AtaquePokemon.query.get(id_pokemon_ataque)
    if not ataque_pokemon:
        abort(404)  # Si no se encuentra la combinación, devolver 404
    result = {
        'id_pokemon_ataque': ataque_pokemon.id_pokemon_ataque,
        'id_ataque': ataque_pokemon.id_ataque,
        'id_pokemon': ataque_pokemon.id_pokemon
    }
    return jsonify(result)

# Ruta para obtener todas las cartas
@app.route('/api/cartas', methods=['GET'])
def get_cartas():
    cartas = Carta.query.all()
    result = []

    for carta in cartas:
        carta_data = {
            'id_carta': carta.id_carta,
            'id_pokemon': carta.id_pokemon,
            'foto_carta': carta.foto_carta  # Ruta de la imagen de la carta
        }
        result.append(carta_data)

    return jsonify(result)


# Ruta para obtener una carta por su ID
@app.route('/api/cartas/<int:id_carta>', methods=['GET'])
def get_carta(id_carta):
    carta = Carta.query.get(id_carta)
    if not carta:
        abort(404)  # Si no se encuentra la carta, devolver un error 404

    # Construir el diccionario de datos de la carta
    result = {
        'id_carta': carta.id_carta,
        'id_pokemon': carta.id_pokemon,
        'foto_carta': carta.foto_carta  # Ruta de la imagen de la carta
    }

    return jsonify(result)

# Ruta para obtener un rango de cartas por sus IDs
@app.route('/api/cartas/rango/<int:id_inicio>/<int:id_fin>', methods=['GET'])
def get_cartas_rango(id_inicio, id_fin):
    if id_inicio >= id_fin:
        abort(400, "ID de inicio debe ser menor que ID final")

    # Filtrar cartas en el rango especificado
    cartas = Carta.query.filter(Carta.id_carta >= id_inicio, Carta.id_carta <= id_fin).all()

    if not cartas:
        abort(404, "No se encontraron cartas en el rango especificado")

    # Construir lista de resultados
    resultado_cartas = []
    for carta in cartas:
        resultado_carta = {
            'id_carta': carta.id_carta,
            'id_pokemon': carta.id_pokemon,
            'foto_carta': carta.foto_carta  # Ruta de la imagen de la carta
        }
        resultado_cartas.append(resultado_carta)

    return jsonify(resultado_cartas)

# Ruta para obtener todos los líderes de gimnasio
@app.route('/api/lideres_gimnasio', methods=['GET'])
def get_lideres_gimnasio():
    lideres = LiderGimnasio.query.all()
    if not lideres:
        abort(404)  # Si no se encuentran líderes, devolver 404

    result = []
    for lider in lideres:
        if isinstance(lider.medalla, bytes):
            medalla_base64 = base64.b64encode(lider.medalla).decode('utf-8')
        elif isinstance(lider.medalla, str):
            # Si medalla es una cadena, debes convertirla a bytes antes de codificarla
            medalla_base64 = base64.b64encode(lider.medalla.encode('utf-8')).decode('utf-8')
        else:
            medalla_base64 = None

        lider_data = {
            'id_lider': lider.id_lider,
            'nombre_lider': lider.nombre_lider,
            'tipo_lider': lider.tipo_lider,
            'medalla': medalla_base64
        }
        result.append(lider_data)

    return jsonify(result)

# Ruta para obtener un líder de gimnasio por su ID
@app.route('/api/lideres_gimnasio/<int:id_lider>', methods=['GET'])
def get_lider_gimnasio(id_lider):
    lider = LiderGimnasio.query.get(id_lider)
    if not lider:
        abort(404)  # Si no se encuentra el líder, devolver 404

    if isinstance(lider.medalla, bytes):
        medalla_base64 = base64.b64encode(lider.medalla).decode('utf-8')
    elif isinstance(lider.medalla, str):
        # Si medalla es una cadena, conviértela a bytes antes de codificar en base64
        medalla_base64 = base64.b64encode(lider.medalla.encode('utf-8')).decode('utf-8')
    else:
        medalla_base64 = None

    result = {
        'id_lider': lider.id_lider,
        'nombre_lider': lider.nombre_lider,
        'tipo_lider': lider.tipo_lider,
        'medalla': medalla_base64
    }

    return jsonify(result)

# Ruta para obtener todas las medallas
@app.route('/api/medallas', methods=['GET'])
def get_medallas():
    medallas = Medalla.query.all()
    result = [{'id_medalla': m.id_medalla,
               'id_usuario': m.id_usuario,
               'medalla': m.medalla} for m in medallas]
    return jsonify(result)

# Ruta para obtener todas las medallas por ID de usuario
@app.route('/api/medallas/usuario/<int:id_usuario>', methods=['GET'])
def get_medallas_by_user_id(id_usuario):
    medallas = Medalla.query.filter_by(id_usuario=id_usuario).all()
    if not medallas:
        abort(404)  # Si no se encuentran medallas para el usuario, devolver 404
    results = []
    for medalla in medallas:
        result = {
            'id_medalla': medalla.id_medalla,
            'id_usuario': medalla.id_usuario,
            'medalla': medalla.medalla
        }
        results.append(result)
    return jsonify(results)


#winBattle
# Verificar si existe la medalla y agregarla si no existe
@app.route('/api/medallas', methods=['POST'])
def add_medalla():
    if not request.json or 'id_usuario' not in request.json or 'medalla' not in request.json:
        abort(400)  # Bad request si los datos son incorrectos

    id_usuario = request.json['id_usuario']
    medalla = request.json['medalla']

    # Verificar si ya existe una medalla con los mismos datos
    existing_medalla = Medalla.query.filter_by(id_usuario=id_usuario, medalla=medalla).first()
    if existing_medalla:
        return jsonify({'message': 'La medalla ya existe'}), 409  # Conflicto

    nueva_medalla = Medalla(id_usuario=id_usuario, medalla=medalla)
    db.session.add(nueva_medalla)

    try:
        db.session.commit()
        return jsonify({'message': 'Medalla agregada correctamente'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error al agregar la medalla'}), 500  # Error interno del servidor


# Incrementar sobres, xp y monedas
@app.route('/api/medallas/incrementar', methods=['POST'])
def incrementar_valores():
    if not request.json or 'id_usuario' not in request.json:
        abort(400)  # Bad request si los datos son incorrectos

    id_usuario = request.json['id_usuario']

    # Incrementar el valor del campo SOBRES en 1 y XP en 50 para el usuario correspondiente
    usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
    if usuario:
        usuario.sobres += 1
        usuario.xp += 50
        db.session.add(usuario)

    # Incrementar el valor del campo monedas en 150 para el usuario correspondiente
    tienda = Tienda.query.filter_by(id_usuario=id_usuario).first()
    if tienda:
        tienda.monedas += 150
    else:
        tienda = Tienda(id_usuario=id_usuario, monedas=150)
        db.session.add(tienda)

    try:
        db.session.commit()
        return jsonify({'message': 'Incrementos realizados correctamente'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error al realizar los incrementos'}), 500  # Error interno del servidor


# Ruta para obtener todos los registros de la Pokedex
@app.route('/api/pokedex', methods=['GET'])
def get_pokedex():
    pokedex_entries = Pokedex.query.all()
    result = [{'id_pokedex': p.id_pokedex,
               'id_usuario': p.id_usuario,
               'id_pokemon': p.id_pokemon} for p in pokedex_entries]
    return jsonify(result)

# Ruta para obtener un registro de la Pokedex por su ID
@app.route('/api/pokedex/user/<int:id_usuario>', methods=['GET'])
def get_pokedex_by_user(id_usuario):
    pokedex_entries = Pokedex.query.filter_by(id_usuario=id_usuario).all()
    if not pokedex_entries:
        abort(404)  # Si no se encuentran registros para ese usuario, devolver 404
    # Crear una lista para almacenar los resultados
    results = []
    for pokedex_entry in pokedex_entries:
        result = {
            'id_pokedex': pokedex_entry.id_pokedex,
            'id_usuario': pokedex_entry.id_usuario,
            'id_pokemon': pokedex_entry.id_pokemon
        }
        results.append(result)
    return jsonify(results)

# Ruta para borrar un registro de la Pokedex por su ID
@app.route('/api/pokedex/delete/<int:id_pokedex>', methods=['DELETE'])
def delete_pokedex_entry(id_pokedex):
    # Buscar la entrada de la Pokedex por su ID
    pokedex_entry = Pokedex.query.get(id_pokedex)
    if not pokedex_entry:
        abort(404, "No se encontró la entrada de la Pokedex con el ID proporcionado")

    # Eliminar la entrada de la Pokedex
    db.session.delete(pokedex_entry)
    db.session.commit()

    return jsonify({'message': 'La entrada de la Pokedex ha sido eliminada correctamente'}), 200

# Ruta para agregar un nuevo registro a la Pokedex de un usuario
@app.route('/api/pokedex/user/<int:id_usuario>/add', methods=['POST'])
def add_pokemon_to_pokedex(id_usuario):
    data = request.get_json()

    if 'id_pokemon' not in data:
        abort(400)  # Si no se proporciona el id_pokemon en los datos JSON, devolver error 400

    id_pokemon = data['id_pokemon']

    # Verificar si el usuario ya tiene este pokemon en su Pokedex
    existing_entry = Pokedex.query.filter_by(id_usuario=id_usuario, id_pokemon=id_pokemon).first()

    if existing_entry:
        return jsonify({'message': f'El usuario ya tiene registrado el Pokémon con id {id_pokemon}'}), 400

    # Crear una nueva entrada en la Pokedex
    new_entry = Pokedex(id_usuario=id_usuario, id_pokemon=id_pokemon)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(
        {'message': f'Pokémon con id {id_pokemon} agregado correctamente a la Pokedex del usuario {id_usuario}'}), 201

# Ruta para agregar un nuevo registro a la Pokedex
@app.route('/api/pokedex', methods=['POST'])
def add_pokedex_entry():
    if not request.json or 'id_usuario' not in request.json or 'id_pokemon' not in request.json:
        abort(400)  # Bad request si los datos son incorrectos

    id_usuario = request.json['id_usuario']
    id_pokemon = request.json['id_pokemon']

    new_entry = Pokedex(id_usuario=id_usuario, id_pokemon=id_pokemon)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Entrada de Pokedex agregada correctamente'}), 201

# Ruta para obtener todos los Pokémon
@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    pokemon_list = Pokemon.query.all()
    result = []
    for p in pokemon_list:
        pokemon_data = {
            'id_pokemon': p.id_pokemon,
            'nombre_pokemon': p.nombre_pokemon,
            'tipo_pokemon': p.tipo_pokemon,
            'ps': p.ps,
            'velocidad': p.velocidad,
            'defensa': p.defensa,
            'foto_pokemon': blob_to_base64(p.foto_pokemon) if p.foto_pokemon else None
        }
        result.append(pokemon_data)
    return jsonify(result)

# Ruta para obtener un Pokémon por su ID
@app.route('/api/pokemon/<int:id_pokemon>', methods=['GET'])
def get_pokemon_by_id(id_pokemon):
    pokemon = Pokemon.query.get(id_pokemon)
    if not pokemon:
        abort(404)  # Si no se encuentra el Pokémon, devolver 404
    result = {
        'id_pokemon': pokemon.id_pokemon,
        'nombre_pokemon': pokemon.nombre_pokemon,
        'tipo_pokemon': pokemon.tipo_pokemon,
        'ps': pokemon.ps,
        'velocidad': pokemon.velocidad,
        'defensa': pokemon.defensa,
        'foto_pokemon': blob_to_base64(pokemon.foto_pokemon) if pokemon.foto_pokemon else None
    }
    return jsonify(result)

def blob_to_base64(blob_data):
    if blob_data:
        # Codificar el blob en base64 y luego decodificarlo a utf-8
        return base64.b64encode(blob_data).decode('utf-8')
    return None

# Ruta para obtener todos los registros de Pokémon por líder
@app.route('/api/pokemon_lider', methods=['GET'])
def get_pokemon_lider():
    pokemon_lider_list = PokemonLider.query.all()
    result = [{'id_lider_pokemon': pl.id_lider_pokemon,
               'id_lider': pl.id_lider,
               'id_pokemon': pl.id_pokemon} for pl in pokemon_lider_list]
    return jsonify(result)

# Ruta para obtener todos los registros de Pokémon por líder por su ID de líder
@app.route('/api/pokemon_lider/<int:id_lider>', methods=['GET'])
def get_pokemon_lider_by_id(id_lider):
    pokemon_lider_list = PokemonLider.query.filter_by(id_lider=id_lider).all()
    if not pokemon_lider_list:
        abort(404)  # Si no se encuentra ningún registro, devolver 404

    result = []
    for pokemon_lider in pokemon_lider_list:
        pokemon_data = {
            'id_lider_pokemon': pokemon_lider.id_lider_pokemon,
            'id_lider': pokemon_lider.id_lider,
            'id_pokemon': pokemon_lider.id_pokemon
        }
        result.append(pokemon_data)

    return jsonify(result)

# Ruta para obtener una tienda por su ID
@app.route('/api/tienda/<int:id_usuario>', methods=['GET'])
def get_tienda_by_id(id_usuario):
    tienda = Tienda.query.filter_by(id_usuario=id_usuario).first()
    if not tienda:
        abort(404)  # Si no se encuentra la tienda, devolver 404
    result = {
        'id_usuario': tienda.id_usuario,
        'monedas': tienda.monedas,
        'cantidad_pokecoins': tienda.cantidad_pokecoins
    }
    return jsonify(result)

# Ruta para agregar una nueva tienda
@app.route('/api/tienda', methods=['POST'])
def add_tienda():
    if not request.json or 'id_usuario' not in request.json or 'monedas' not in request.json or 'cantidad_pokecoins' not in request.json:
        abort(400)  # Bad request si los datos son incorrectos

    id_usuario = request.json['id_usuario']
    monedas = request.json['monedas']
    cantidad_pokecoins = request.json['cantidad_pokecoins']

    # Buscar la tienda del usuario por ID_USUARIO
    tienda = Tienda.query.filter_by(id_usuario=id_usuario).first()

    if not tienda:
        abort(404)  # Si no se encuentra la tienda del usuario, devolver error 404 Not Found

    # Modificar los valores de monedas y cantidad_pokecoins según lo recibido en la solicitud
    tienda.monedas += monedas
    tienda.cantidad_pokecoins += cantidad_pokecoins

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({'message': 'Tienda modificada correctamente'}), 200

# Ruta para obtener un usuario por su nombre de usuario
@app.route('/api/usuario/nombre/<nombre_usuario>', methods=['GET'])
def get_usuario_by_nombre(nombre_usuario):
    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
    if not usuario:
        abort(404)  # Si no se encuentra el usuario, devolver 404
    result = {
        'id_usuario': usuario.id_usuario,
        'nombre_usuario': usuario.nombre_usuario,
        'mail': usuario.mail,
        'contraseña': usuario.contraseña,
        'admin': usuario.admin,
        'sobres': usuario.sobres,
        'xp': usuario.xp,#
        'fecha_apertura': usuario.fecha_apertura#Incluimos el campo 'sobres'
    }
    return jsonify(result)

# Ruta para obtener un usuario por su ID
@app.route('/api/usuario/<int:id_usuario>', methods=['GET'])
def get_usuario_by_id(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        abort(404)  # Si no se encuentra el usuario, devolver 404
    result = {
        'id_usuario': usuario.id_usuario,
        'nombre_usuario': usuario.nombre_usuario,
        'mail': usuario.mail,
        'contraseña': usuario.contraseña,
        'admin': usuario.admin,
        'sobres': usuario.sobres,
        'xp': usuario.xp,# Incluimos el campo 'sobres'
        'fecha_apertura': usuario.fecha_apertura
    }
    return jsonify(result)

#register
from datetime import datetime

@app.route('/api/usuario', methods=['POST'])
def add_usuario():
    # Comprobar si la solicitud es JSON y tiene los campos necesarios
    if not request.json or 'nombre_usuario' not in request.json or 'mail' not in request.json or 'contraseña' not in request.json:
        abort(400)  # Bad request si los datos son incorrectos

    # Extraer datos de la solicitud JSON
    nombre_usuario = request.json['nombre_usuario']
    mail = request.json['mail']
    contraseña = request.json['contraseña']
    admin = request.json.get('admin', False)
    sobres = request.json.get('sobres', 3)
    xp = request.json.get('xp', 0)  # Valor predeterminado de sobres: 0
    fecha_apertura = datetime.now()  # Fecha actual

    # Crear una instancia de Usuario y establecer la contraseña hasheada
    nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, mail=mail, admin=admin, sobres=sobres, xp=xp, fecha_apertura=fecha_apertura)
    nuevo_usuario.set_password(contraseña)  # Establecer la contraseña hasheada

    # Guardar el nuevo usuario en la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Construir el JSON de respuesta con el ID y nombre del usuario insertado
    respuesta = {
        'id_usuario': nuevo_usuario.id_usuario,
        'nombre_usuario': nuevo_usuario.nombre_usuario
    }

    # Después de devolver la respuesta, realizar un insert en la tabla TIENDA
    tienda_nuevo_usuario = Tienda(id_usuario=respuesta['id_usuario'], monedas=0, cantidad_pokecoins=0)

    # Guardar la nueva entrada de tienda en la base de datos
    db.session.add(tienda_nuevo_usuario)
    db.session.commit()

    # Devolver la respuesta como JSON junto con el código de estado 201 (Created)
    return jsonify(respuesta), 201

#restar sobres
@app.route('/api/usuario/restar_sobres/<int:id_usuario>', methods=['POST'])
def restar_sobres_usuario(id_usuario):
    # Buscar el usuario por su ID
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        abort(404)  # Si no se encuentra el usuario, devolver error 404

    # Restar 1 a la cantidad de sobres
    if usuario.sobres > 0:
        usuario.sobres -= 1

    # Guardar los cambios en la base de datos
    db.session.commit()

    # Devolver la respuesta JSON con el nuevo estado de sobres del usuario
    result = {
        'id_usuario': usuario.id_usuario,
        'nombre_usuario': usuario.nombre_usuario,
        'mail': usuario.mail,
        'admin': usuario.admin,
        'sobres': usuario.sobres,
        'xp': usuario.xp,
        'fecha_apertura': usuario.fecha_apertura
        # Agregar más campos si es necesario
    }
    return jsonify(result), 200

# Ruta para obtener las cartas de un usuario por su ID
@app.route('/api/cartas/usuario/<int:id_usuario>', methods=['GET'])
def get_cartas_usuario(id_usuario):
    # Buscar todos los ID de Pokémon en la Pokedex del usuario
    pokedex_entries = Pokedex.query.filter_by(id_usuario=id_usuario).all()
    if not pokedex_entries:
        abort(404, "No se encontraron Pokémon en la Pokedex para este usuario")

    # Recopilar todos los IDs de Pokémon del usuario
    pokemon_ids = [entry.id_pokemon for entry in pokedex_entries]

    # Buscar cartas que correspondan a los IDs de Pokémon del usuario
    cartas_usuario = Carta.query.filter(Carta.id_pokemon.in_(pokemon_ids)).all()

    if not cartas_usuario:
        abort(404, "No se encontraron cartas para los Pokémon en la Pokedex de este usuario")

    # Preparar la respuesta JSON
    result = []
    for carta in cartas_usuario:
        carta_data = {
            'id_carta': carta.id_carta,
            'id_pokemon': carta.id_pokemon,
            'foto_carta': carta.foto_carta  # Ruta de la imagen de la carta
        }
        result.append(carta_data)

    return jsonify(result)

# Ruta para obtener cartas repetidas de un usuario por su ID
@app.route('/api/cartas/usuario/dupes/<int:id_usuario>', methods=['GET'])
def get_cartas_usuario_dupes(id_usuario):
    # Buscar todos los ID de Pokémon en la Pokedex del usuario
    pokedex_entries = Pokedex.query.filter_by(id_usuario=id_usuario).all()

    if not pokedex_entries:
        abort(404, "No se encontraron Pokémon en la Pokedex para este usuario")

    # Preparar la respuesta JSON
    result = []

    # Diccionario para mantener el recuento de id_pokemon, id_pokedex y la cantidad de cartas repetidas
    pokemon_info = {}

    # Iterar sobre las entradas de la Pokedex
    for entry in pokedex_entries:
        id_pokemon = entry.id_pokemon
        id_pokedex = entry.id_pokedex

        # Incrementar el contador para el id_pokemon actual
        if id_pokemon in pokemon_info:
            pokemon_info[id_pokemon]['id_pokedex'].append(id_pokedex)
            pokemon_info[id_pokemon]['count'] += 1
        else:
            pokemon_info[id_pokemon] = {
                'id_pokedex': [id_pokedex],
                'count': 1
            }

    # Iterar sobre los id_pokemon y verificar si hay duplicados
    for id_pokemon, info in pokemon_info.items():
        # Verificar si hay más de una entrada para este id_pokemon
        if info['count'] > 1:
            # Obtener todas las cartas asociadas a este id_pokemon
            cartas_repetidas = Carta.query.filter_by(id_pokemon=id_pokemon).all()

            # Preparar los datos de la carta repetida
            carta_data = {
                'id_pokemon': id_pokemon,
                'id_pokedex': info['id_pokedex'],  # Agregar los id_pokedex de los duplicados
                'cantidad_repetidas': info['count'],  # Agregar la cantidad de cartas repetidas
                'cartas_repetidas': [{
                    'id_carta': carta.id_carta,
                    'foto_carta': carta.foto_carta  # Ruta de la imagen de la carta
                } for carta in cartas_repetidas]
            }

            # Agregar los datos de la carta repetida al resultado
            result.append(carta_data)

    if not result:
        abort(404, "No se encontraron cartas repetidas para los Pokémon en la Pokedex de este usuario")

    return jsonify(result)

#login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contraseña = data.get('contrasena')

    if nombre_usuario is None or contraseña is None:
        return jsonify({"estado": "error", "mensaje": "Usuario o contraseña faltantes"}), 400

    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if not usuario:
        return jsonify({"estado": "error", "mensaje": "Usuario no encontrado"}), 404

    # Verificar la contraseña
    if (contraseña == usuario.contraseña or
        check_password_hash(usuario.contraseña, contraseña)):
        # Si la contraseña coincide, actualiza la contraseña hasheada si no está hasheada
        if not usuario.contraseña.startswith('$'):  # Verifica si la contraseña está hasheada
            usuario.set_password(contraseña)
            db.session.commit()

        # Preparar los datos del usuario para la respuesta
        user_data = {
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "mail": usuario.mail,
            "admin": usuario.admin,
            "sobres": usuario.sobres,
            "xp": usuario.xp,
            'fecha_apertura': usuario.fecha_apertura
            # Agregar más campos si es necesario
        }

        return jsonify({"estado": "ok", "usuario": user_data}), 200
    else:
        return jsonify({"estado": "error", "mensaje": "Usuario o contraseña incorrectos"}), 401


# Ruta para obtener todos los registros de la Pokedex por el ID de usuario y el ID de Pokémon
@app.route('/api/pokedex/user/<int:id_usuario>/pokemon/<int:id_pokemon>', methods=['GET'])
def get_pokedex_by_user_and_pokemon(id_usuario, id_pokemon):
    pokedex_entries = Pokedex.query.filter_by(id_usuario=id_usuario, id_pokemon=id_pokemon).all()
    if not pokedex_entries:
        abort(404)  # Si no se encuentran registros para ese usuario y Pokémon, devolver 404
    
    # Crear una lista para almacenar los resultados
    results = []
    for pokedex_entry in pokedex_entries:
        result = {
            'id_pokedex': pokedex_entry.id_pokedex,
            'id_usuario': pokedex_entry.id_usuario,
            'id_pokemon': pokedex_entry.id_pokemon
        }
        results.append(result)
    
    return jsonify(results), 200

#FECHA APERTURA
@app.route('/api/usuario/actualizar_fecha_apertura/<int:id_usuario>', methods=['PUT'])
def actualizar_fecha_apertura(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        # Actualizar el campo fecha_apertura con la fecha actual
        usuario.fecha_apertura = datetime.datetime.now()

        db.session.commit()

        return jsonify({'message': 'Fecha de apertura actualizada correctamente'}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para obtener la fecha de apertura de un usuario específico
@app.route('/api/usuario/fecha_apertura/<int:id_usuario>', methods=['GET'])
def obtener_fecha_apertura(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        fecha_apertura = usuario.fecha_apertura.strftime("%Y-%m-%d %H:%M:%S")  # Formatea la fecha como string
        return jsonify({'fecha_apertura': fecha_apertura}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para obtener todos los Pokémon de un usuario por su ID
@app.route('/api/pokemon/usuario/<int:id_usuario>', methods=['GET'])
def get_pokemon_by_user_id(id_usuario):
    # Buscar todos los IDs de Pokémon en la Pokédex del usuario
    pokedex_entries = Pokedex.query.filter_by(id_usuario=id_usuario).all()
    if not pokedex_entries:
        abort(404, "No se encontraron Pokémon en la Pokédex para este usuario")

    # Recopilar todos los IDs de Pokémon del usuario
    pokemon_ids = [entry.id_pokemon for entry in pokedex_entries]

    # Buscar los detalles de cada Pokémon en la tabla "POKEMON" utilizando los IDs de Pokémon obtenidos
    pokemon_list = Pokemon.query.filter(Pokemon.id_pokemon.in_(pokemon_ids)).all()

    if not pokemon_list:
        abort(404, "No se encontraron Pokémon para los IDs en la Pokédex de este usuario")

    # Preparar la respuesta JSON
    result = []
    for p in pokemon_list:
        pokemon_data = {
            'id_pokemon': p.id_pokemon,
            'nombre_pokemon': p.nombre_pokemon,
            'tipo_pokemon': p.tipo_pokemon,
            'ps': p.ps,
            'velocidad': p.velocidad,
            'defensa': p.defensa,
            'foto_pokemon': p.foto_pokemon,
            'foto_pokemon_back': p.foto_pokemon_back
        }
        result.append(pokemon_data)

    return jsonify(result)


# Ruta para obtener los datos de un Pokémon junto con sus ataques por su ID
@app.route('/api/pokemon/ataques/<int:id_pokemon>', methods=['GET'])
def get_pokemon_with_attacks(id_pokemon):
    # Buscar los datos del Pokémon por su ID
    pokemon = Pokemon.query.get(id_pokemon)
    if not pokemon:
        abort(404, "No se encontró el Pokémon con el ID proporcionado")

    # Buscar todos los ataques asociados a este Pokémon
    ataques_pokemon = AtaquePokemon.query.filter_by(id_pokemon=id_pokemon).all()

    if not ataques_pokemon:
        abort(404, "No se encontraron ataques para este Pokémon")

    # Preparar la respuesta JSON
    result = {
        'id_pokemon': pokemon.id_pokemon,
        'nombre_pokemon': pokemon.nombre_pokemon,
        'tipo_pokemon': pokemon.tipo_pokemon,
        'ps': pokemon.ps,
        'velocidad': pokemon.velocidad,
        'defensa': pokemon.defensa,
        'foto_pokemon': pokemon.foto_pokemon,
        'foto_pokemon_back': pokemon.foto_pokemon_back,
        'ataques': []
    }

    # Buscar los detalles de cada ataque asociado a este Pokémon
    for ataque_pokemon in ataques_pokemon:
        ataque = Ataque.query.get(ataque_pokemon.id_ataque)
        if not ataque:
            continue
        ataque_data = {
            'id_ataque': ataque.id_ataque,
            'nombre_ataque': ataque.nombre_ataque,
            'tipo_ataque': ataque.tipo_ataque,
            'pp': ataque.pp,
            'daño': ataque.daño
        }
        result['ataques'].append(ataque_data)

    return jsonify(result)

@app.route('/api/lider/Battle/<int:id_lider>')
def obtener_datos_lider(id_lider):
    lider = LiderGimnasio.query.filter_by(id_lider=id_lider).first()
    if lider:
        pokemons_lider = PokemonLider.query.filter_by(id_lider=id_lider).all()
        data = {
            'nombre_lider': lider.nombre_lider,
            'tipo_lider': lider.tipo_lider,
            'medalla': lider.medalla,
            'pokemons': []
        }
        for pokemon_lider in pokemons_lider:
            pokemon = Pokemon.query.filter_by(id_pokemon=pokemon_lider.id_pokemon).first()
            if pokemon:
                ataques_pokemon = AtaquePokemon.query.filter_by(id_pokemon=pokemon.id_pokemon).all()
                ataques = []
                for ataque_pokemon in ataques_pokemon:
                    ataque = Ataque.query.filter_by(id_ataque=ataque_pokemon.id_ataque).first()
                    if ataque:
                        ataques.append({
                            'nombre_ataque': ataque.nombre_ataque,
                            'tipo_ataque': ataque.tipo_ataque,
                            'pp': ataque.pp,
                            'daño': ataque.daño
                        })
                data['pokemons'].append({
                    'nombre_pokemon': pokemon.nombre_pokemon,
                    'tipo_pokemon': pokemon.tipo_pokemon,
                    'ps': pokemon.ps,
                    'velocidad': pokemon.velocidad,
                    'defensa': pokemon.defensa,
                    'foto_pokemon': pokemon.foto_pokemon,
                    'foto_pokemon_back': pokemon.foto_pokemon_back,
                    'ataques': ataques
                })
        return jsonify(data)
    else:
        return jsonify({'mensaje': 'Líder de gimnasio no encontrado'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
