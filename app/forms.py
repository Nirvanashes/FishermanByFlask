from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import EmailField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login in")


class RegisterForm(LoginForm):
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField(label="Register")


class SetProjectForm(FlaskForm):
    name = StringField(label="Project Name", validators=[DataRequired()])
    # todo 多层级目录后续再实现
    # parent_project = SelectField(label="Parent project")  # 需要实例化后传递给表单
    submit = SubmitField(label="Submit")
