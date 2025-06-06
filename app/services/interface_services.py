from flask_login import current_user
from sqlalchemy import select, func

from app.extensions import db, paginate
from app.forms import InterfaceForm
from app.schema import Interface, TestCase
from app.services.project_services import ProjectServices


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
            # headers=form.headers.data,
            belong_project_id=form.belong_project.data,
            create_user_id=current_user.id,
            description=form.description.data
        )
        db.session.add(new_interface)
        db.session.commit()
        return new_interface

    @staticmethod
    def edit_interface(interface_id, form: InterfaceForm):
        interface = InterfaceServices.get_interface_by_id(interface_id)
        interface.interface_method = form.interface_method.data
        interface.interface_address = form.interface_address.data
        interface.interface_name = form.interface_name.data
        interface.belong_project_id = form.belong_project.data
        interface.create_user_id = current_user.id
        interface.description = form.description.data
        db.session.commit()
        return interface

    @staticmethod
    def make_interface_form():
        form = InterfaceForm()
        projects_list = ProjectServices.get_all_projects()
        form.belong_project.choices = [(project.id, project.name) for project in projects_list]
        return form

    @staticmethod
    def del_interface(interface_id):
        interface = InterfaceServices.get_interface_by_id(interface_id)
        db.session.delete(interface)
        db.session.commit()
        return True

    @staticmethod
    def get_all_interface_by_page(page):
        return paginate(query=select(Interface), page=page)

    @staticmethod
    def fitter_testcase_by_interface():
        result = db.session.execute(
            select(
                Interface.interface_name.label("interface_name"),
                func.count(TestCase.id).label("testcase_count")
            )
            .join(TestCase, Interface.testcases)
            .group_by(Interface.id)
        ).fetchall()
        return result
