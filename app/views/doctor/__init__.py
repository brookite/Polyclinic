from flask import Blueprint, render_template

view = Blueprint('doctor', __name__, url_prefix ='/doctor')


@view.route("/lk")
def stats():
    return render_template("admin.html")


@view.route("/plan")
def admin():
    return render_template("admin.html")