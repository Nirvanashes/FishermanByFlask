from flask import Blueprint, render_template, redirect, url_for, request

from app.forms import InterfaceTestcaseFrom
from app.services.interface_services import InterfaceServices
from app.services.testcase_services import TestCaseServices

case_route = Blueprint("case", __name__)


@case_route.route("/all-case")
def get_all_case():
    all_case = TestCaseServices.get_all_case()
    return render_template("case.html", all_case=all_case)


@case_route.route("/all-case/<int:interface_id>")
def get_all_case_by_interface(interface_id):
    all_case = TestCaseServices.get_case_by_interface(interface_id)
    return render_template("case.html", all_case=all_case)


@case_route.route("/add-case", methods=["GET", "POST"])
def add_case():
    interface_id = request.args.get("interface_id")
    form = InterfaceTestcaseFrom(
        belong_interface=interface_id
    )
    interface_list = InterfaceServices.get_all_interface()
    form.belong_interface.choices = [(interface.id, interface.interface_name) for interface in interface_list]
    if form.validate_on_submit():
        new_case = TestCaseServices.add_case(form)
        return redirect(url_for("interface.show_interface", interface_id=form.belong_interface.data))
    return render_template("make-case.html", form=form)


@case_route.route("/edit-case/<int:case_id>", methods=["GET", "POST"])
def edit_case(case_id):
    case = TestCaseServices.get_case_by_id(case_id)
    form = InterfaceTestcaseFrom(
        testcase_name=case.testcase_name,
        headers=case.headers,
        params=case.params,
        expected_results=case.expected_results,
        description=case.description,
        belong_interface=case.belong_interface_id,
    )
    interface_list = InterfaceServices.get_all_interface()
    form.belong_interface.choices = [(interface.id, interface.interface_name) for interface in interface_list]
    if form.validate_on_submit():
        TestCaseServices.edit_case(case_id, form)
        return redirect(url_for("interface.show_interface", interface_id=form.belong_interface.data))
    return render_template("make-case.html", form=form)

@case_route.route("/del-case")
def del_case():
    case_id = request.args.get("case_id")
    interface_id = request.args.get("interface_id")
    TestCaseServices.del_case(case_id)
    return redirect(url_for("interface.show_interface", interface_id=interface_id))
