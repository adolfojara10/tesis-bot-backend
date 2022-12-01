from flask import Flask, render_template
from forms import RegistrateMainUserForm, LoginForm, RegistrateSubUserForm, RegistrateCameraForm, RegistrateHouseForm
from waitress import serve
import time
from config import *  # importamod token
import telebot
import threading
from telebot.types import ForceReply

app = Flask(__name__)

app.config['SECRET_KEY'] = "073f2f7a1f493b43348ad5dacbfa9768"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

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

@app.route("/registrarUsuario")
def registrarUsuario():
    form = RegistrateMainUserForm()

    return render_template("registrarUsuario.html", title="Registrar", form=form)


@app.route("/login")
def registrarUsuario():
    form = LoginForm()

    return render_template("login.html", title="Login", form=form)


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

    

