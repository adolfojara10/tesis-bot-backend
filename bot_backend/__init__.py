from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from bot_backend.config import *  # importamod token
import telebot


app = Flask(__name__)

app.config['SECRET_KEY'] = "073f2f7a1f493b43348ad5dacbfa9768"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./site.db"

db = SQLAlchemy(app)

#bcypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
global usuario_autenticado, usuarioSeleccionado
usuarioSeleccionado = None

from bot_backend import routes