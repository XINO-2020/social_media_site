#blog/ __init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from PIL import Image

################


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
Migrate(app,db)
###########33login config###########3333
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

################register blueprints
from blogs.users.views import users
from blogs.error_pages.handlers import error_pages
from blogs.core.views import core
from blogs.blogpost.views import blogpost


app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blogpost)
