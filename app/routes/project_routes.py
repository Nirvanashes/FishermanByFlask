from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.forms import SetProjectForm
from app.services.project_services import ProjectServices

pj_bp = Blueprint("project", __name__)


@pj_bp.route("/projects")
def get_all_projects():
    projects = ProjectServices.get_all_projects()
    return render_template("project.html", projects=projects)


@pj_bp.route("/add-project", methods=["GET", "POST"])
@login_required
def add_project():
    form = SetProjectForm()
    if form.validate_on_submit():
        new_project = ProjectServices.add_project(
            name=form.name.data,
            user=current_user
        )
        return redirect(url_for("project.get_all_projects"))
    return render_template("make-project.html", form=form)


@pj_bp.route("/edit-project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = ProjectServices.get_project_by_id(project_id)
    form = SetProjectForm(
        name=project.name
    )
    if form.validate_on_submit():
        new_project = ProjectServices.edit_project(
            name=form.name.data,
            project=project
        )
        return redirect(url_for("project.get_all_projects"))
    return render_template("make-project.html", form=form)


@pj_bp.route("/del-project")
@login_required
def del_project():
    project_id = request.args.get("project_id")
    ProjectServices.del_project(project_id)
    return redirect(url_for("project.get_all_projects"))
