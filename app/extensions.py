from datetime import datetime, timezone, timedelta
from typing import Optional
from flask import Flask, session
from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from flask_mail import Mail
from flask_caching import Cache
from config import Config


class Base(DeclarativeBase):
    # 为每张表生成以下字段
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    created_time: Mapped[datetime] = mapped_column(
        # default=lambda: datetime.now(timezone(timedelta(hours=8))),  # 使用lambda确保每次调用获取新时间
        default=lambda: datetime.now(),
        comment="创建时间"
    )

    updated_time: Mapped[Optional[datetime]] = mapped_column(
        onupdate=lambda: datetime.now(),
        default=lambda: datetime.now(),  # 使用lambda确保每次调用获取新时间
        comment="更新时间"
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
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    mail.init_app(app)
    cache.init_app(app)


def paginate(query: Select, page: int = 1, per_page: int = Config.ITEMS_PER_PAGE):
    """
    通用分页函数
    :param query: SQLAlchemy查询对象
    :param page: 当前页码
    :param per_page: 每页数量
    :return: 分页对象
    """
    return db.paginate(
        query,
        page=page,
        per_page=per_page,
        error_out=False
    )