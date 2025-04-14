from flask_login import current_user
from sqlalchemy import select

from app.extensions import db
from app.forms import InterfaceForm
from app.schema import Interface


class InterfaceServices:
    @staticmethod
    def get_all_interface():
        return db.session.scalars(select(Interface)).all()

    @staticmethod
    def get_all_interface_with_project(project_id):
        return db.session.scalars(select(Interface).where(Interface.belong_project_id == project_id))

    @staticmethod
    def get_interface_by_id(interface_id):
        return db.get_or_404(Interface, interface_id)

    @staticmethod
    def get_testcase_by_interface_id(interface_id):
        return db.get_or_404(Interface, interface_id).testcases

    @staticmethod
    def add_interface(form: InterfaceForm):
        new_interface = Interface(
            interface_name=form.interface_name.data,
            interface_address=form.interface_address.data,
            interface_method=form.interface_method.data,
            headers=form.headers.data,
            belong_project_id=form.belong_project.data,
            create_user_id=current_user.id
        )
        db.session.add(new_interface)
        db.session.commit()
        return new_interface
