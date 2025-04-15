from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import EmailField, PasswordField, URLField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """用于注册相关表单"""
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login in")


class RegisterForm(LoginForm):
    """用于登录相关表单"""
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField(label="Register")


class SetProjectForm(FlaskForm):
    """用于所属项目相关表单"""
    name = StringField(label="Project Name", validators=[DataRequired()])
    # todo 多层级目录后续再实现
    # parent_project = SelectField(label="Parent project")  # 需要实例化后传递给表单
    submit = SubmitField(label="Submit")


class InterfaceForm(FlaskForm):
    belong_project = SelectField(label="Belong Project", coerce=int)  # 需要实例化后传递给表单
    interface_name = StringField(label="Interface Name", validators=[DataRequired()])
    interface_address = URLField(label="Interface Address", validators=[DataRequired()])
    interface_method = SelectField(label="Interface Method",
                                 choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
                                 validators=[DataRequired()])
    # params_type = SelectField("Params Type", choices=["FORM", "JSON"])
    headers = StringField(label="Interface Headers")
    submit = SubmitField(label="Submit")


class InterfaceTestcaseFrom(FlaskForm):
    belong_interface = SelectField(label="Belong Interface", coerce=int)  # 需要实例化后传递给表单
    testcase_name = StringField(label="Testcase Name", validators=[DataRequired()])
    headers = StringField(label="Headers")
    params = StringField(label="Request Params")
    expected_results = StringField(label="Expected results", validators=[DataRequired()])

