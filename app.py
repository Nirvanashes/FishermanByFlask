from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from app.extensions import init_extensions, db
from app.auth.models import User
from config import Config
from app.auth.routes import auth_bp

app = Flask(__name__,template_folder="app/templates")
app.config.from_object(Config)
init_extensions(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
