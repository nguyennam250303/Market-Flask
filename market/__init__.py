from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

SECRET_KEY = os.urandom(12)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = SECRET_KEY


db = SQLAlchemy(app)

login = LoginManager(app)

login.login_view = "login_page"
login.login_message_category = "info"



from market import routes
















