from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from app.extensions import db


class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
