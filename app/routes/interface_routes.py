from flask import Flask, Blueprint, render_template, url_for, redirect, request

from app.forms import InterfaceForm
from app.services.interface_services import InterfaceServices
from app.services.project_services import ProjectServices

interface_bp = Blueprint("interface", __name__)


# @interface_bp.route("/interface")
# def interface_list():
#     all_interface = InterfaceServices.get_all_interface()
#     return render_template("interface.html", interface=all_interface)


@interface_bp.route("/get-all-interface")
def get_all_interface():
    all_interface = InterfaceServices.get_all_interface()
    return render_template("interface.html", interface=all_interface)


@interface_bp.route("/filter-by-project")
def filter_by_project(project_id):
    all_interface = InterfaceServices.get_all_interface_with_project(project_id)
    return all_interface


@interface_bp.route("/interface-info/<int:interface_id>")
def show_interface(interface_id):
    interface_info = InterfaceServices.get_interface_by_id(interface_id)
    return render_template("interface-info.html", interface=interface_info)


@interface_bp.route("/add-interface", methods=["GET", "POST"])
def add_interface():
    form = InterfaceForm()
    projects_list = ProjectServices.get_all_projects()
    form.belong_project.choices = [(project.id, project.name) for project in projects_list]
    # form = InterfaceServices.make_interface_form()
    if form.validate_on_submit():
        new_interface = InterfaceServices.add_interface(form)
        return redirect(url_for("interface.get_all_interface"))
    return render_template("make-interface.html", form=form)


@interface_bp.route("/edit-interface/<int:interface_id>", methods=["GET", "POST"])
def edit_interface(interface_id):
    interface = InterfaceServices.get_interface_by_id(interface_id)
    form = InterfaceForm(
        interface_name=interface.interface_name,
        interface_method=interface.interface_method,
        interface_address=interface.interface_address,
        description=interface.description,
        belong_project=interface.belong_project_id
    )
    projects_list = ProjectServices.get_all_projects()
    form.belong_project.choices = [(project.id, project.name) for project in projects_list]
    if form.validate_on_submit():
        interface = InterfaceServices.edit_interface(interface_id, form)
        return redirect(url_for("interface.get_all_interface"))
    return render_template("make-interface.html", form=form)


@interface_bp.route("/del-interface")
def del_interface():
    interface_id = request.args.get("interface_id")
    InterfaceServices.del_interface(interface_id)
    return redirect(url_for("interface.get_all_interface"))
