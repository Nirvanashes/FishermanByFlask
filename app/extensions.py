from flask import Flask, session
from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_caching import Cache


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
bootstrap = Bootstrap5()
login_manager = LoginManager()
mail = Mail()
cache = Cache()


def init_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
