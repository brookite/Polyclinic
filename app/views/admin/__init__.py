from flask import Blueprint, render_template
from app.utils.login import role_required, get_user, get_logged_in
from app.utils.enums import Role

view = Blueprint('admin', __name__, url_prefix ='/')


@view.route("/stats")
@role_required([Role.EMPLOYEE])
def stats():
    return render_template("stats.html")


@view.route("/admin")
@role_required([Role.EMPLOYEE])
def admin():
    return render_template("admin.html")


@view.route("/admin_workshifts")
@role_required([Role.EMPLOYEE])
def admin_workshifts():
    return render_template("admin_workshifts.html")


@view.route("/admin_doctors")
@role_required([Role.EMPLOYEE])
def admin_doctors():
    return render_template("admin_doctors.html")


@view.route("/admin_medicaments")
@role_required([Role.EMPLOYEE])
def admin_medicaments():
    return render_template("admin_medicaments.html")


@view.route("/admin_diseases")
@role_required([Role.EMPLOYEE])
def admin_diseases():
    return render_template("admin_diseases.html")


@view.route("/admin_employees")
@role_required([Role.EMPLOYEE])
def admin_employees():
    return render_template("admin_employees.html")


@view.route("/admin_offices")
@role_required([Role.EMPLOYEE])
def admin_offices():
    return render_template("admin_offices.html")
