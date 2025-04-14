from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user
from app.forms import RegisterForm, LoginForm
from app.services.auth_services import AuthServices
from app.utils.security import check_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = AuthServices.get_user_by_email(form.email.data)
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("auth.login"))
        new_user = AuthServices.create_user(
            email=form.email.data,
            name=form.name.data,
            password=form.password.data
        )
        login_user(new_user)
        return render_template("index.html")
    return render_template("login.html", form=form, is_login=True)


@auth_bp.route(rule="/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthServices.get_user_by_email(form.email.data)
        if user and check_password(user.password, form.password.data):
            login_user(user)
            return render_template("index.html")
        else:
            flash("the email or password is incorrect, please try again.")
            return redirect(url_for("auth.login"))
    return render_template("login.html", form=form, is_login=True)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login", is_login=False))
