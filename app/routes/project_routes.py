from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.forms import SetProjectForm
from app.services.project_services import ProjectServices

pj_bp = Blueprint("project", __name__)


@pj_bp.route("/projects")
def get_all_projects():
    projects = ProjectServices.get_all_projects()
    return projects


@pj_bp.route("/add-project",methods=["GET","POST"])
# @login_required
def add_project():
    form = SetProjectForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_project = ProjectServices.add_project(
                name=form.name.data,
                user=current_user
            )
            return redirect(url_for("project.add_project"))
    return render_template("project.html", form=form)
