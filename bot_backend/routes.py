from flask import render_template, flash, redirect, url_for
from bot_backend import app, bot, db
from flask_bcrypt import Bcrypt
from bot_backend.forms import RegistrateMainUserForm, LoginForm, RegistrateSubUserForm, RegistrateCameraForm, RegistrateHouseForm
from bot_backend.models import Usuario, Casa, Camara
from telebot.types import ForceReply
from flask_login import login_user, current_user, logout_user

bcrypt = Bcrypt(app)
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


@app.route("/registrarUsuarioPrimario", methods=['POST', "GET"])
def registrarUsuarioPrimario():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrateMainUserForm()

    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        usuario = Usuario(nombre = form.nombre.data, apellido=form.apellido.data, 
                    email=form.email.data, password=hashed_pw, tipo="Primario")

        db.session.add(usuario)
        db.session.commit()

        flash(f"Cuenta creada con éxito", category="success")

        return redirect(url_for("login"))

    return render_template("registrarUsuarioPrimario.html", title="Registrar", form=form)


@app.route("/registrarUsuarioSecundario", methods=['POST', "GET"])
def registrarUsuarioSecundario():

    form = RegistrateSubUserForm()

    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        usuario = Usuario(nombre = form.nombre.data, apellido=form.apellido.data, 
                    email=form.email.data, password=hashed_pw, tipo="Secundario")

        db.session.add(usuario)
        db.session.commit()

        flash(f"Cuenta creada con éxito", category="success")

        return redirect(url_for("login"))

    return render_template("registrarUsuarioSecundario.html", title="Registrar-usuario", form=form)




@app.route("/login", methods=['POST', "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data) and usuario.tipo == "Primario":
            
            login_user(usuario, remember=True)
            return redirect(url_for("home"))
        else:
            flash("Credenciales erroneos o no tiene permiso. Revise sus datos", category="warning")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/registrarCamara")
def registrarCamara():

    form = RegistrateCameraForm()

    return render_template("registrarCamara.html", title="Casa", form=form)


@app.route("/registrarCasa", methods=['POST', "GET"])
def registrarCasa():

    form1 = RegistrateHouseForm()
    form2 = RegistrateCameraForm()
    form = [form1, form2]

    if form[0].validate_on_submit():
        
        casa = Casa(direccion=form[0].direccion.data, numero_direccion=form[0].numero_direccion.data)

        db.session.add(casa)
        db.session.commit()

        c = db.session.query(Casa).order_by(Casa.id.desc()).first()
        flash("Casa y cámaras creadas con exito", category="success")

        print(form[1])

        return redirect(url_for("home"))
            

    return render_template("registrarCasa.html", title="Casa", form=form)


@app.route("/cuenta")
def cuenta():
    return render_template("cuenta.html", title="Cuenta")


@app.route("/about")
def about():
    return render_template("about.html", title="about")