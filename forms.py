from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrateMainUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo(password)])

    tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])
    
    submit = SubmitField("Crear usuario")

class RegistrateSubUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo(password)])

    tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])

    id_casa = IntegerField("ID de la casa: ", validators=[DataRequired()])
    
    submit = SubmitField("Crear usuario")


class LoginForm(FlaskForm):

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])

    submit = SubmitField("Iniciar sesión")
    

class RegistrateHouseForm(FlaskForm):

    direccion = StringField("Dirección: ", validators=[DataRequired(), Length(2,150)])
    
    submit = SubmitField("Enviar")

class RegistrateCameraForm(FlaskForm):

    jardin = IntegerField("Número de cámaras en el jardín: ", validators=[DataRequired()])
    garage = IntegerField("Número de cámaras en el garage: ", validators=[DataRequired()])
    sala_comunal = IntegerField("Número de cámaras en la sala comunal: ", validators=[DataRequired()])
    comedor_comunal = IntegerField("Número de cámaras en el comedor: ", validators=[DataRequired()])
    cocina = IntegerField("Número de cámaras en la cocina: ", validators=[DataRequired()])
    tv = IntegerField("Número de cámaras en el sala de tv: ", validators=[DataRequired()])
    dormitorio = IntegerField("Número de cámaras en los dormitorios: ", validators=[DataRequired()])
    calle = IntegerField("Número de cámaras hacia la calle: ", validators=[DataRequired()])
    entrada = IntegerField("Número de cámaras en la entrda: ", validators=[DataRequired()])
        
    submit = SubmitField("Enviar")

    

    
    



