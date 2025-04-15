from flask_login import current_user
from sqlalchemy import select

from app.extensions import db
from app.forms import InterfaceTestcaseFrom
from app.schema import TestCase


class TestCaseServices:
    @staticmethod
    def get_all_case():
        return db.session.scalars(TestCase).all()

    @staticmethod
    def get_case_by_interface(interface_id):
        return db.session.scalars(select(TestCase).where(TestCase.belong_interface_id == interface_id)).all()

    @staticmethod
    def get_case_by_id(case_id):
        return db.get_or_404(TestCase, case_id)

    @staticmethod
    def add_case(form: InterfaceTestcaseFrom):
        new_case = TestCase(
            testcase_name=form.testcase_name.data,
            headers=form.headers.data,
            params=form.params.data,
            expected_results=form.expected_results.data,
            description=form.description.data,
            belong_interface_id=form.belong_interface.data,
            create_user_id=current_user.id

        )
        db.session.add(new_case)
        db.session.commit()
        return new_case

    @staticmethod
    def edit_case(case_id,form: InterfaceTestcaseFrom):
        case = TestCaseServices.get_case_by_id(case_id)
        case.testcase_name = form.testcase_name.data
        case.params = form.params.data
        case.headers = form.headers.data
        case.expected_results = form.expected_results.data
        case.description = form.description.data
        case.belong_interface_id = form.belong_interface.data
        case.create_user_id = current_user.id
        db.session.commit()
        return case

    @staticmethod
    def del_case(case_id):
        case = TestCaseServices.get_case_by_id(case_id)
        db.session.delete(case)
        db.session.commit()
