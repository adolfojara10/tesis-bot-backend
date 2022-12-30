from bot_backend import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):

    return Usuario.query.get(int(usuario_id))


class Usuario(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(75), nullable=False)
    apellido = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    telegram_chat_id = db.Column(db.String(20), nullable=True)

    casa_id = db.Column(db.Integer, db.ForeignKey("casa.id"), nullable=True)




    def __repr__(self) -> str:
        return  f"Usuario('{self.nombre}', '{self.apellido}', '{self.tipo}', '{self.id}')"


class Casa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(150), nullable=False)
    numero_direccion = db.Column(db.String(12), nullable=False)

    usuarios = db.relationship('Usuario', backref='casa', lazy=True)

    camaras = db.relationship('Camara', backref="camara", lazy=True)



    def __repr__(self) -> str:
        return  f"Casa('{self.direccion}', '{self.numero_direccion}', '{self.id}')"

class Camara(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(150), nullable=False)
    #numero_direccion = db.Column(db.String(12), nullable=False)
    casa_id = db.Column(db.Integer, db.ForeignKey("casa.id"), nullable=False)


    def __repr__(self) -> str:
        return  f"Camara('{self.id}', '{self.ubicacion}')"