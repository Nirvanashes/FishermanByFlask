from typing import List
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from app.extensions import db


class UserInfo(db.Model):
    __abstract__ = True
    create_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # update_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


# class User(UserMixin,db.Model):
class User(UserMixin, db.Model):
    # id: Mapped[int] = mapped_column(Integer, primary_key=True) #迁移至Base类中统一生成
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    default_project: Mapped[int] = mapped_column(Integer, nullable=True)

    created_projects: Mapped[List["Project"]] = relationship(back_populates="create_user",
                                                             foreign_keys="[Project.create_user_id]"
                                                             )


class Project(UserInfo):
    """用于记录项目"""
    name: Mapped[str] = mapped_column(String(50), unique=True)
    # parent_project_id: Mapped[int] = mapped_column(Integer, nullable=True)

    create_user: Mapped["User"] = relationship(back_populates="created_projects"
                                               )
    interfaces: Mapped[List["Interface"]] = relationship(back_populates="belong_project")


class Interface(UserInfo):
    """记录接口"""
    interface_name: Mapped[str] = mapped_column(String)
    interface_address: Mapped[str] = mapped_column(String, unique=True)
    interface_method: Mapped[str] = mapped_column(String(10))
    # headers: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)

    belong_project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    belong_project: Mapped["Project"] = relationship(back_populates="interfaces")
    testcases: Mapped[List["TestCase"]] = relationship(back_populates="belong_interface")


class TestCase(UserInfo):
    testcase_name: Mapped[str] = mapped_column(String)
    headers: Mapped[str] = mapped_column(String)
    params: Mapped[str] = mapped_column(String)
    # params_type: Mapped[str] = mapped_column(String, nullable=True)
    expected_results: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)

    belong_interface_id: Mapped[int] = mapped_column(ForeignKey("interface.id"))
    belong_interface: Mapped["Interface"] = relationship(back_populates="testcases")


class TestResult(UserInfo):
    pass


class TestResultInfo(UserInfo):
    pass
