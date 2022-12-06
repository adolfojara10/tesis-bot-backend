from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bot_backend.config import *  # importamod token
import telebot


app = Flask(__name__)

app.config['SECRET_KEY'] = "073f2f7a1f493b43348ad5dacbfa9768"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./site.db"

db = SQLAlchemy(app)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

from bot_backend import routes