from flask_login import current_user
from sqlalchemy import select

from app.extensions import db
from app.schema import Project


class ProjectServices:
    @staticmethod
    def get_all_level1_projects():
        return db.session.scalars(select(Project).where(Project.parent_project_id is None)).all()

    @staticmethod
    def get_all_level1_project_list_with_null():
        result = ProjectServices.get_all_level1_projects()
        projects = [(project.id, project.name) for project in result]
        projects.append((None, " "))
        return projects.reverse()

    @staticmethod
    def get_all_projects():
        return db.session.scalars(select(Project)).all()

    @staticmethod
    def add_project(name,user):
        new_project = Project(
            name=name,
            create_user=user
        )
        db.session.add(new_project)
        db.session.commit()
        return new_project
