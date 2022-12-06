from flask import render_template, flash, redirect, url_for
from bot_backend import app, bot
from bot_backend.forms import RegistrateMainUserForm, LoginForm, RegistrateSubUserForm, RegistrateCameraForm, RegistrateHouseForm
from bot_backend.models import Usuario, Casa, Camara
from telebot.types import ForceReply

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
        bot.register_next_step_handler(msg, preguntar_password)
    else:
        cuenta.append(message.text)
        markup = ForceReply()

        msg = bot.send_message(message.chat.id, "Escribe tu contraseña", reply_markup=markup)
        bot.register_next_step_handler(msg, verificar_cuenta)



def verificar_cuenta(message):
    cuenta.append(message.text)
    print(cuenta)





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