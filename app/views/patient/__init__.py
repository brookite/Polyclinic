from flask import Blueprint, render_template, url_for


view = Blueprint('patient', __name__, url_prefix ='/')


@view.route("/lk")
def lk():
    return render_template("lk.html")


@view.route("/patient_file")
def patient_file():
    return render_template("lk.html")
