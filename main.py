from flask import Flask, render_template
from sqlalchemy import select

from app.extensions import init_extensions, db
from app.services.project_services import ProjectServices
from config import Config
# from app.schema import User,Project,
from app.routes.project_routes import pj_bp
from app.routes.auth_routes import auth_bp
from app.routes.interface_routes import interface_bp
from app.routes.testcase_route import case_route
import plotly.express as px
import pandas as pd

app = Flask(__name__, template_folder="app/templates")
app.config.from_object(Config)
init_extensions(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(pj_bp)
app.register_blueprint(interface_bp)
app.register_blueprint(case_route)


@app.route("/")
def welcome():
    data = ProjectServices.fitter_interface_by_product()
    df = pd.DataFrame(data, columns=['project_name', 'interface_count'])
    fig = px.bar(
        data_frame=df,
        x="project_name",
        y="interface_count",
        title="项目接口数量统计",
        labels={
            "project_name": "项目名称",
            "interface_count": "接口数量"
        },
        color="project_name",
        text="interface_count"
    )
    fig.update_layout(
        xaxis_title="项目",
        yaxis_title="接口数量",
        hovermode="x"
    )
    chart_html = fig.to_html(full_html=False)
    return render_template("index.html", chart_html=chart_html)


if __name__ == "__main__":
    app.run()
