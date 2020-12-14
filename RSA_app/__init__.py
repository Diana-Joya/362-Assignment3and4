from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# DB Settings
app.config['SECRET_KEY'] = '27f8f8s3j3018aks19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Manages User Authentication
bcrypt = Bcrypt(app)

# Manages User Sessions
login_manager = LoginManager(app)
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return None

from RSA_app import routing
from RSA_app import tester_script
