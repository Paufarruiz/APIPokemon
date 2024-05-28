from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Ataque(db.Model):
    __tablename__ = 'ATAQUES'  # Nombre de la tabla en la base de datos
    id_ataque = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_ataque = db.Column(db.String(20), nullable=False)
    tipo_ataque = db.Column(db.String(20), nullable=False)
    pp = db.Column(db.Integer, nullable=False)
    daño = db.Column(db.Integer, nullable=False)

class AtaquePokemon(db.Model):
    __tablename__ = 'ATAQUE_POKEMON'
    id_pokemon_ataque = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ataque = db.Column(db.Integer, nullable=False)
    id_pokemon = db.Column(db.Integer, nullable=False)

class Carta(db.Model):
    __tablename__ = 'CARTA'
    id_carta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pokemon = db.Column(db.Integer, nullable=False)
    foto_carta = db.Column(db.String(255), nullable=False) 

class LiderGimnasio(db.Model):
    __tablename__ = 'LIDER_GIMNASIO'
    id_lider = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_lider = db.Column(db.String(20), nullable=False)
    tipo_lider = db.Column(db.String(20), nullable=False)
    medalla = db.Column(db.String(20), nullable=False)
    foto_medalla = db.Column(db.BLOB, nullable=False)

class Medalla(db.Model):
    __tablename__ = 'MEDALLAS'
    id_medalla = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    medalla = db.Column(db.String(255), nullable=False)

class Pokedex(db.Model):
    __tablename__ = 'POKEDEX'
    id_pokedex = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_pokemon = db.Column(db.Integer, nullable=False)

class Pokemon(db.Model):
    __tablename__ = 'POKEMON'
    id_pokemon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_pokemon = db.Column(db.String(20), nullable=False)
    tipo_pokemon = db.Column(db.String(20), nullable=False)
    ps = db.Column(db.Integer, nullable=False)
    velocidad = db.Column(db.Integer, nullable=False)
    defensa = db.Column(db.Integer, nullable=False)
    foto_pokemon = db.Column(db.String(255), nullable=False)
    foto_pokemon_back = db.Column(db.String(255), nullable=False)

class PokemonLider(db.Model):
    __tablename__ = 'POKEMON_LIDER'
    id_lider_pokemon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_lider = db.Column(db.Integer, nullable=False)
    id_pokemon = db.Column(db.Integer, nullable=False)

class Tienda(db.Model):
    __tablename__ = 'TIENDA'
    id_usuario = db.Column(db.Integer, primary_key=True, nullable=False)
    monedas = db.Column(db.Integer, nullable=False)
    cantidad_pokecoins = db.Column(db.Integer, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'USUARIO'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(40), nullable=False)
    contraseña = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    sobres = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    fecha_apertura = db.Column(db.DateTime)

    def set_password(self, contraseña):
        # Hashea la contraseña antes de almacenarla
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        # Verifica si la contraseña ingresada coincide con la almacenada,
        # considerando que la contraseña puede estar almacenada en texto sin formato o hasheada
        if self.contraseña is None:
            return False  # Si la contraseña no está configurada, no puede coincidir
        if self.contraseña.startswith('$'):
            # La contraseña está hasheada, usar check_password_hash
            return check_password_hash(self.contraseña, contraseña)
        else:
            # La contraseña está almacenada en texto sin formato, comparar directamente
            return self.contraseña == contraseña