from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bot_backend.models import Usuario


class RegistrateMainUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo("password")])

    #tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])
    
    submit = SubmitField("Crear usuario")

    def validate_email(self, email):

        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("Email ya registrado!")
        
        

class RegistrateSubUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo("password")])

    #tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])

    id_casa = IntegerField("ID de la casa: ", validators=[DataRequired()])
    
    submit = SubmitField("Crear usuario")

    def validate_email(self, email):

        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("Email ya registrado!")


class LoginForm(FlaskForm):

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])

    submit = SubmitField("Iniciar sesión")

    def validate_primario(self, email):

        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario.tipo == "Secundario":
            raise ValidationError("No tienes permiso para iniciar sesión")
    

class RegistrateHouseForm(FlaskForm):

    direccion = StringField("Dirección: ", validators=[DataRequired(), Length(2,150)])
    numero_direccion = StringField("Número dirección: ", validators=[Length(2,12)])
    
    submit = SubmitField("Enviar")

class RegistrateCameraForm(FlaskForm):

    '''jardin = IntegerField("Número de cámaras en el jardín: ", validators=[DataRequired()], default=0)
    garage = IntegerField("Número de cámaras en el garage: ", validators=[DataRequired()], default=0)
    sala_comunal = IntegerField("Número de cámaras en la sala comunal: ", validators=[DataRequired()], default=0)
    comedor_comunal = IntegerField("Número de cámaras en el comedor: ", validators=[DataRequired()], default=0)
    cocina = IntegerField("Número de cámaras en la cocina: ", validators=[DataRequired()], default=0)
    tv = IntegerField("Número de cámaras en el sala de tv: ", validators=[DataRequired()], default=0)
    dormitorio = IntegerField("Número de cámaras en los dormitorios: ", validators=[DataRequired()], default=0)
    calle = IntegerField("Número de cámaras hacia la calle: ", validators=[DataRequired()], default=0)
    entrada = IntegerField("Número de cámaras en la entrda: ", validators=[DataRequired()], default=0)'''
        
    jardin = IntegerField("Número de cámaras en el jardín: ", default=0)
    garage = IntegerField("Número de cámaras en el garage: ", default=0)
    sala_comunal = IntegerField("Número de cámaras en la sala comunal: ", default=0)
    comedor_comunal = IntegerField("Número de cámaras en el comedor: ", default=0)
    cocina = IntegerField("Número de cámaras en la cocina: ", default=0)
    tv = IntegerField("Número de cámaras en el sala de tv: ", default=0)
    dormitorio = IntegerField("Número de cámaras en los dormitorios: ", default=0)
    calle = IntegerField("Número de cámaras hacia la calle: ", default=0)
    entrada = IntegerField("Número de cámaras en la entrda: ", default=0)
    submit = SubmitField("Enviar")

    

    
    



