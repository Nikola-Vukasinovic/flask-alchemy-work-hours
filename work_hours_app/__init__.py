import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY') 
#############################################################
############# DATABASE SETUP ################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#############################################################


db = SQLAlchemy(app)

Migrate(app, db)

#############################################################
############# LOGIN MANAGER #################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


#############################################################


from work_hours_app.core.views import core
from work_hours_app.users.views import users
from work_hours_app.entries.views import entries


app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(entries)
