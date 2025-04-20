from flask_login import current_user
from sqlalchemy import select, func

from app.extensions import db, paginate
from app.schema import Project, Interface


class ProjectServices:
    @staticmethod
    def get_all_projects():
        return db.session.scalars(select(Project)).all()

    @staticmethod
    def get_all_projects_by_page(page):
        return paginate(query=select(Project), page=page)

    @staticmethod
    def get_project_by_id(project_id: int):
        return db.get_or_404(Project, project_id)

    @staticmethod
    def get_all_level1_projects():
        return db.session.scalars(select(Project).where(Project.parent_project_id is None)).all()

    @staticmethod
    def select_project():
        # result = ProjectServices.get_all_level1_projects()
        result = ProjectServices.get_all_projects()
        projects = [(project.id, project.name) for project in result]
        projects.append((None, " "))
        return projects.reverse()

    @staticmethod
    def add_project(name, user):
        new_project = Project(
            name=name,
            create_user=user
        )
        db.session.add(new_project)
        db.session.commit()
        return new_project

    @staticmethod
    def edit_project(project, name):
        project.name = name
        project.create_user = current_user
        project.create_user_id = current_user.id
        db.session.commit()
        return True

    @staticmethod
    def del_project(project_id):
        project = ProjectServices.get_project_by_id(project_id)
        db.session.delete(project)
        db.session.commit()
        return True

    @staticmethod
    def fitter_interface_by_product():
        result = db.session.execute(
            select(
                Project.name.label('project_name'),
                func.count(Interface.id).label('interface_count')
            )
            .join(Interface, Project.interfaces)
            .group_by(Project.id)
        ).fetchall()
        return result
