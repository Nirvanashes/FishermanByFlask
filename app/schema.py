from typing import List
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from app.extensions import db


class User(UserMixin, db.Model):
    # id: Mapped[int] = mapped_column(Integer, primary_key=True) #迁移至Base类中统一生成
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    created_projects: Mapped[List["Project"]] = relationship(back_populates="create_user")


class Project(db.Model):
    name: Mapped[str] = mapped_column(String(50))
    parent_project_id: Mapped[int] = mapped_column(Integer,nullable=False)
    create_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    create_user: Mapped["User"] = relationship(back_populates="created_projects")
