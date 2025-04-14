from flask import Flask, Blueprint, render_template, url_for

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


@interface_bp.route("/add-interface", methods=["GET", "POST"])
def add_interface():
    form = InterfaceForm()
    projects_list = ProjectServices.get_all_projects()
    form.belong_project.choices = [(project.id,project.name) for project in projects_list]
    if form.validate_on_submit():
        new_interface = InterfaceServices.add_interface(form)
        return render_template("interface.html")
    return render_template("add-interface.html", form=form)
