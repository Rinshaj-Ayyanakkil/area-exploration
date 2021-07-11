from flask import Blueprint, render_template, redirect, session, request, url_for, Blueprint
from functools import wraps

from app.utils.dbconnect import select

login_bp = Blueprint("login", __name__)


def login_required(func):
    @wraps(func)
    def warpper(*args, **kwargs):

        user = session.get("user")
        if user is None:
            return redirect("/login"), 301

        return func(user, *args, **kwargs)

    return warpper


# function to render homepage
@login_bp.route("/")
@login_bp.route("/home")
@login_required
def home(user):

    return render_template("home-page.html", user=user), 200


# render login page
@login_bp.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user") is not None:
        return redirect(url_for("site.login.logout_page"))

    if request.method == "GET":

        return render_template("login-page.html"), 200

    if request.method == "POST":

        req_username = request.form["loginUsername"]
        req_password = request.form["loginPassword"]

        query = "SELECT * FROM login WHERE username=%s"
        user = select(query, req_username)

        error: str = ""

        if user is None:
            error = "User not found"
            return f"<script>alert({error})</script>"

        if user["password"] != req_password:
            error = "Password incorrect"
            return f"<script>alert({error})</script>"

        if user["user_type"] != "admin":
            error = "Access for admins only"
            return f"<script>alert({error})</script>"

        secure_user = {k: v for k, v in user.items() if k not in ("password")}
        session["user"] = secure_user
        return redirect(url_for("site.login.home")), 302


# render logout confirmation page
@login_bp.route("/logout")
@login_required
def logout_page(user):

    return render_template("logout-page.html", user=user), 200


@login_bp.route("/logout/confirm")
@login_required
def logout(user):
    session.clear()
    return redirect(url_for("site.login.home")), 302


@login_bp.route("/error")
@login_required
def render_error_page(user):
    return render_template("error-page.html"), 200
