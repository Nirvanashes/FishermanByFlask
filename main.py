from importlib import reload

from flask import Flask, render_template
from flask_login import login_required
from sqlalchemy import select

from app.extensions import init_extensions, db
from app.services.interface_services import InterfaceServices
from app.services.project_services import ProjectServices
from app.services.testcase_services import TestCaseServices
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
@login_required
def welcome():
    # -------------------------------------------------项目接口统计图表------------------------------------------------- #
    fitter_interface_by_product = ProjectServices.fitter_interface_by_product()
    df_interface_by_product = pd.DataFrame(fitter_interface_by_product, columns=['project_name', 'interface_count'])
    fig_interface_by_product = px.pie(
        data_frame=df_interface_by_product,
        values="interface_count",
        names="project_name",
        title="项目接口数量统计",
        labels={
            "project_name": "项目名称",
            "interface_count": "接口数量"
        },
    )
    fig_interface_by_product.update_layout(height=500)

    # fig_interface_by_product = px.bar(
    #     data_frame=df_interface_by_product,
    #     x="project_name",
    #     y="interface_count",
    #     title="项目接口数量统计",
    #     labels={
    #         "project_name": "项目名称",
    #         "interface_count": "接口数量"
    #     },
    #     color="project_name",
    #     text="interface_count"
    # )
    # fig_interface_by_product.update_layout(
    #     xaxis_title="项目",
    #     yaxis_title="接口数量",
    #     hovermode="x"
    # )
    html_interface_by_product = fig_interface_by_product.to_html(full_html=False)

    # -------------------------------------------------接口用例统计图表------------------------------------------------- #
    fitter_testcase_by_interface = InterfaceServices.fitter_testcase_by_interface()
    df_testcase_by_interface = pd.DataFrame(fitter_testcase_by_interface, columns=['interface_name', 'testcase_count'])
    fig_testcase_by_interface = px.pie(
        data_frame=df_testcase_by_interface,
        values="testcase_count",
        names="interface_name",
        title="接口用例数量统计",
        labels={
            "interface_name": "接口名称",
            "testcase_count": "用例数量"
        }
    )
    fig_testcase_by_interface.update_layout(autosize=True, height=500)

    # fig_testcase_by_interface = px.bar(
    #     data_frame=df_testcase_by_interface,
    #     x="interface_name",
    #     y="testcase_count",
    #     title="接口用例数量统计",
    #     labels={
    #         "interface_name": "接口名称",
    #         "testcase_count": "用例数量"
    #     },
    #     color="interface_name",
    #     text="testcase_count"
    # )
    # fig_testcase_by_interface.update_layout(
    #     xaxis_title="接口名称",
    #     yaxis_title="用例数量",
    #     hovermode="x"
    # )
    html_testcase_by_interface = fig_testcase_by_interface.to_html(full_html=False)

    # -------------------------使用Sunburst图表统一展示项目-接口-用例三种数据的相对关系------------------------- #

    return render_template("index.html",
                           html_interface_by_product=html_interface_by_product,
                           html_testcase_by_interface=html_testcase_by_interface
                           )


if __name__ == "__main__":
    app.run()
