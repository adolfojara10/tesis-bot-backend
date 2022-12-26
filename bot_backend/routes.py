from flask import render_template, flash, redirect, url_for, request
from bot_backend import app, bot, db
from flask_bcrypt import Bcrypt
from bot_backend.forms import RegistrateMainUserForm, LoginForm, RegistrateSubUserForm, RegistrateCameraForm, RegistrateHouseForm
from bot_backend.models import Usuario, Casa, Camara
from telebot.types import ForceReply
from flask_login import login_user, current_user, logout_user, login_required

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

            """global usuario_autenticado
            usuario_autenticado = usuario"""
            
            login_user(usuario, remember=True)

            next_page = request.args.get("next")

            return redirect(next_page) if next_page else redirect(url_for("home"))
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
        
        #actualizo al usuario con su casa
        usu = current_user
        usu.casa_id=c.id
        print(current_user)
        #db.session.commit()


        ubicacion_cams = ["jardin", "garage","sala_comunal","comedor_comunal",
                    "cocina","tv","dormitorio","calle","entrada"]
        for i in range(9):
            if form2[ubicacion_cams[i]].data == 1:
                cam = Camara(ubicacion=ubicacion_cams[i], casa_id=c.id)
                db.session.add(cam)
                db.session.commit()
            elif form2[ubicacion_cams[i]].data > 1:
                for j in range(form2[ubicacion_cams[i]].data):
                    cam = Camara(ubicacion=ubicacion_cams[i], casa_id=c.id)
                    db.session.add(cam)
                    db.session.commit()

        
        flash("Casa y cámaras creadas con exito", category="success")

        

        return redirect(url_for("home"))
            

    return render_template("registrarCasa.html", title="Casa", form=form)


@app.route("/cuenta")
@login_required
def cuenta():

    #print(current_user.casa_id)

    casa_cu = Casa.query.filter_by(id=current_user.casa_id).first()



    camaras = {}
    for cam in range(len(casa_cu.camaras)):
        if cam == 0:
            camaras[casa_cu.camaras[cam].ubicacion] = 1
        else:
            if camaras.get(casa_cu.camaras[cam].ubicacion) != None:
                camaras[casa_cu.camaras[cam].ubicacion] = camaras[casa_cu.camaras[cam].ubicacion]+1
            else:
                camaras[casa_cu.camaras[cam].ubicacion] = 1

    usuarios = []

    for us in casa_cu.usuarios:
        if us.id != current_user.id:
            usuarios.append(us)

    


    return render_template("cuenta.html", title="Cuenta", casa_cu=casa_cu, camaras=camaras, usuarios=usuarios)


'''
actualizar
'''

@app.route("/actualizarCamaras", methods=['POST', "GET"])
def actualizarCamaras():

    form = RegistrateCameraForm()

    casa_cu = Casa.query.filter_by(id=current_user.casa_id).first()

    camaras = {"jardin":0, "garage":0, "sala_comunal":0, "comedor_comunal":0, "cocina":0, "tv":0,
                "dormitorio":0, "calle":0, "entrada":0}
    for cam in range(len(casa_cu.camaras)):
        if cam == 0:
            camaras[casa_cu.camaras[cam].ubicacion] = 1
        else:
            if camaras.get(casa_cu.camaras[cam].ubicacion) != 0:
                camaras[casa_cu.camaras[cam].ubicacion] = camaras[casa_cu.camaras[cam].ubicacion]+1
            else:
                camaras[casa_cu.camaras[cam].ubicacion] = 1

    #print(camaras)

    if form.validate_on_submit():

        c = casa_cu
        
        ubicacion_cams = ["jardin", "garage","sala_comunal","comedor_comunal",
                    "cocina","tv","dormitorio","calle","entrada"]
        for i in range(9):
            if form[ubicacion_cams[i]].data != 0:
                
                num_insertado = form[ubicacion_cams[i]].data
                ccc = Camara.query.filter_by(ubicacion=ubicacion_cams[i])
                num_existentes = Camara.query.filter_by(ubicacion=ubicacion_cams[i]).count()

                if num_insertado - num_existentes == 0:
                    pass
                elif num_insertado - num_existentes > 0:
                    for j in range(num_insertado - num_existentes):
                        cam = Camara(ubicacion=ubicacion_cams[i], casa_id=c.id)
                        db.session.add(cam)
                        db.session.commit()
                elif num_insertado - num_existentes < 0:
                    for j in range((num_insertado - num_existentes)*-1):
                        db.session.delete(Camara.query.filter_by(ubicacion=ubicacion_cams[i])[-1])
                        db.session.commit()           


            elif form[ubicacion_cams[i]].data == 0:
                try:
                    Camara.query.filter_by(ubicacion=ubicacion_cams[i]).delete()
                    db.session.commit()
                except:
                    pass
                
            '''elif form[ubicacion_cams[i]].data > 1:
                for j in range(form[ubicacion_cams[i]].data):
                    cam = Camara(ubicacion=ubicacion_cams[i], casa_id=c.id)
                    db.session.add(cam)
                    db.session.commit()'''

        
        print(c.camaras)
        flash("Cámaras actualizadas con éxito", category="success")

        

        return redirect(url_for("cuenta"))
    
    return render_template("actualizarCamaras.html", title="Actualizar Cámaras", form=form, camaras=camaras)


@app.route("/about")
def about():
    return render_template("about.html", title="about")