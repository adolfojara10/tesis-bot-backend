from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrateMainUserForm, LoginForm, RegistrateSubUserForm, RegistrateCameraForm, RegistrateHouseForm
from flask_sqlalchemy import SQLAlchemy
import time
from config import *  # importamod token
import telebot
import threading
from telebot.types import ForceReply

app = Flask(__name__)

app.config['SECRET_KEY'] = "073f2f7a1f493b43348ad5dacbfa9768"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)

bot = telebot.TeleBot(TELEGRAM_TOKEN)


class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(75), nullable=False)
    apellido = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

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
        return  f"Casa('{self.id}', '{self.ubicacion}')"

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

global cuenta

# responde al comando \start
@bot.message_handler(commands=["start"])
def cmd_start(message):

    texto = "Bienvido a HAL9000, el chatbot inteligente para tu hogar.\n"
    texto += "/iniciar_sesion para iniciar sesion con tu cuenta. \n"
    texto += "/foto para obtener una foto de alguna cámara. \n"
    texto += "/video para obtener un video de alguna cámara. \n"


    
    bot.send_message(message.chat.id, texto)

@bot.message_handler(commands=["iniciar_sesion"])
def cmd_iniciar_sesion(message):
    global cuenta
    cuenta = []
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "Escribe tu email", reply_markup=markup)

    bot.register_next_step_handler(msg, preguntar_password)


def preguntar_password(message):

    if not "@" in message.text:
        markup = ForceReply()

        msg = bot.send_message(message.chat.id, "Debes digitar un email!! \n Escribe tu email", reply_markup=markup)
        bot.register_next_step_handler(msg, verificar_cuenta)
    else:
        cuenta.append(message.text)
        markup = ForceReply()

        msg = bot.send_message(message.chat.id, "Escribe tu contraseña", reply_markup=markup)
        bot.register_next_step_handler(msg, verificar_cuenta)



def verificar_cuenta(message):
    cuenta.append(message.text)
    print(cuenta)



def recibir_mensajes():
    bot.infinity_polling()
    


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/registrarUsuario", methods=['POST', "GET"])
def registrarUsuario():
    form = RegistrateMainUserForm()

    if form.validate_on_submit():

        flash(f"Cuenta creada con éxito", category="success")

        return redirect(url_for("login"))

    return render_template("registrarUsuario.html", title="Registrar", form=form)


@app.route("/login", methods=['POST', "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == "gavilanesadolfo@gmail.com" and form.password.data == "1234":
            flash("Sesión iniciada con éxito", category="success")

            return redirect(url_for("home"))
        else:
            flash("Credenciales erroneos. Revise sus datos", category="warning")




    return render_template("login.html", title="Login", form=form)

@app.route("/registrarCamara")
def registrarCamara():

    form = RegistrateHouseForm()

    return render_template("registrarCasa.html", title="Casa", form=form)


@app.route("/registrarCasa")
def registrarCasa():

    form = RegistrateHouseForm()

    return render_template("registrarCasa.html", title="Casa", form=form)



@app.route("/about")
def about():
    return render_template("about.html", title="about")


def start_app():
    print("iniciando bot")
    bot.set_my_commands([telebot.types.BotCommand("/start", "Visualizar opciones"),
        telebot.types.BotCommand("/iniciar_sesion","para iniciar sesion con tu cuenta"),
        telebot.types.BotCommand("/foto","para obtener una foto de alguna cámara"),
        telebot.types.BotCommand("/video","para obtener un video de alguna cámara")        
        ])
    # bucle infinito para comprobar si se reciben mensajes nuevos
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()

    print("BOOOT INICIADO")
    app.run()




if __name__ == "__main__":
    

    app_thread = threading.Thread(name="app_thread", target=start_app)
    app_thread.start()

    print("app INICIADO")

    

