from flask import Blueprint, render_template, session
from app.utils.login import role_required, login_required
from app.utils.enums import Role
from app.utils.login import get_logged_in
from app.db.queries import get_patient_by_id
from app.db.authorization import get_user

view = Blueprint('patient', __name__, url_prefix ='/')


@view.route("/lk")
def lk():
    return render_template("lk.html")


@view.route("/patient_file")
def patient_file():
    return render_template("lk.html")


@view.route("/appointment")
@login_required
@role_required([Role.PATIENT])
def appointment():
    user = get_user(get_logged_in())
    patient = get_patient_by_id(user["patient_id"])[0]
    return render_template(
        "appointment.html", 
        patient_name=patient["fio"], 
        patient_phone=patient["phone_number"]
    )
