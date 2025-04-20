from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import EmailField, PasswordField, URLField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """用于注册相关表单"""
    email = EmailField(label="邮箱", validators=[DataRequired()])
    password = PasswordField(label="密码", validators=[DataRequired()])
    submit = SubmitField(label="登录")


class RegisterForm(LoginForm):
    """用于登录相关表单"""
    name = StringField(label="姓名", validators=[DataRequired()])
    submit = SubmitField(label="注册")


class SetProjectForm(FlaskForm):
    """用于所属项目相关表单"""
    name = StringField(label="项目名称", validators=[DataRequired()])
    # todo 多层级目录后续再实现
    # parent_project = SelectField(label="Parent project")  # 需要实例化后传递给表单
    submit = SubmitField(label="提交")


class InterfaceForm(FlaskForm):
    belong_project = SelectField(label="所属项目", coerce=int)  # 需要实例化后传递给表单
    interface_name = StringField(label="接口名称", validators=[DataRequired()])
    interface_address = URLField(label="接口地址", validators=[DataRequired()])
    interface_method = SelectField(label="请求方式",
                                   choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
                                   validators=[DataRequired()])
    description = StringField(label="描述")
    # params_type = SelectField("Params Type", choices=["FORM", "JSON"])
    # headers = StringField(label="Interface Headers")
    submit = SubmitField(label="提交")


class InterfaceTestcaseFrom(FlaskForm):
    belong_interface = SelectField(label="所属接口", coerce=int)  # 需要实例化后传递给表单
    testcase_name = StringField(label="用例名称", validators=[DataRequired()])
    headers = StringField(label="Headers")
    params = StringField(label="请求参数")
    expected_results = StringField(label="预期结果", validators=[DataRequired()])
    description = StringField(label="描述")
    submit = SubmitField(label="提交")
