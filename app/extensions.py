from datetime import datetime, timezone, timedelta
from typing import Optional
from flask import Flask, session
from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, Integer
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, declared_attr, mapped_column, Mapped
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_caching import Cache
from app.utils.utils import beijing_time


class Base(DeclarativeBase):
    # 为每张表生成以下字段
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_time: Mapped[datetime] = mapped_column(
        # default=lambda: datetime.now(timezone(timedelta(hours=8))),  # 使用lambda确保每次调用获取新时间
        default=lambda: datetime.now(),
        comment="创建时间（北京时间）"
    )

    updated_time: Mapped[Optional[datetime]] = mapped_column(
        onupdate=lambda: datetime.now(),
        default=lambda: datetime.now(),  # 使用lambda确保每次调用获取新时间
        comment="更新时间（北京时间）"
    )


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
