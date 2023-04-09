from flask import Blueprint, render_template

view = Blueprint('admin', __name__, url_prefix ='/admin')


@view.route("/stats")
def stats():
    return render_template("stats.html")


@view.route("/admin")
def admin():
    return render_template("admin.html")

