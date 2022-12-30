from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from bot_backend.models import Usuario


class RegistrateMainUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])

    telefono = StringField("Número de teléfono: Ejemplo: 0963204011", validators=[DataRequired(),Length(10,10)])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo("password")])

    #tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])
    
    submit = SubmitField("Crear usuario")

    def validate_email(self, email):

        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("Email ya registrado!")

    def validate_telefono(self, telefono):

        usuario = Usuario.query.filter_by(telefono=telefono.data).first()

        if usuario:
            raise ValidationError("Teléfono ya registrado!")
        
        

class RegistrateSubUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])
    telefono = StringField("Número de teléfono: Ejemplo: 0963204011", validators=[DataRequired(),Length(10,10)])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo("password")])

    #tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])

    #id_casa = IntegerField("ID de la casa: ", validators=[DataRequired()])
    
    submit = SubmitField("Crear usuario")

    def validate_email(self, email):

        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("Email ya registrado!")

    def validate_telefono(self, telefono):

        usuario = Usuario.query.filter_by(telefono=telefono.data).first()

        if usuario:
            raise ValidationError("Teléfono ya registrado!")
        



class EscogerUsuarioActualizar(FlaskForm):
    id = IntegerField("ID del usuario a actualizar", validators=[DataRequired(),NumberRange(min=1, max=10000, message='Invalid length')],default=1)
    submit = SubmitField("Actualizar")


class UpdateSubUserForm(FlaskForm):

    nombre = StringField("Nombre(s): ", validators=[DataRequired(), Length(2,75)])
    apellido = StringField("Apellidos: ", validators=[DataRequired(), Length(2,75)])

    email = StringField("Email: ", validators=[DataRequired(),Email()])
    telefono = StringField("Número de teléfono: Ejemplo: 0963204011", validators=[DataRequired(),Length(10,10)])

    password = PasswordField("Contraseña: ", validators=[DataRequired(), Length(2,32)])
    confirm_password = PasswordField("Confirmar contraseña: ", validators=[DataRequired(), 
                                    Length(2,32), EqualTo("password")])

    #tipo = SelectField("Tipo de usuario: ", choices=[("Primario", "Primario"), ("Secundario", "Secundario")])

    
    submit = SubmitField("Actualizar usuario")

    def validate_email(self, email):

        usuario = Usuario.query.filter_by(email=email.data).count()

        if usuario > 1:
            raise ValidationError("Email ya registrado!")

    def validate_telefono(self, telefono):

        usuario = Usuario.query.filter_by(telefono=telefono.data).count()

        if usuario > 1:
            
            raise ValidationError("Teléfono ya registrado!")




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
        
    jardin = IntegerField("Número de cámaras en el jardín: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    garage = IntegerField("Número de cámaras en el garage: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    sala_comunal = IntegerField("Número de cámaras en la sala comunal: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    comedor_comunal = IntegerField("Número de cámaras en el comedor: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    cocina = IntegerField("Número de cámaras en la cocina: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    tv = IntegerField("Número de cámaras en el sala de tv: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    dormitorio = IntegerField("Número de cámaras en los dormitorios: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    calle = IntegerField("Número de cámaras hacia la calle: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    entrada = IntegerField("Número de cámaras en la entrada: ", validators=[NumberRange(min=0, max=5, message='Invalid length')],default=0)
    submit = SubmitField("Enviar")

