from flask import Blueprint, render_template
from app.db.queries import get_doctor_plan, \
    get_doctor_patient_history, get_doctor_appointments, \
    get_doctor_by_id
from app.utils.login import role_required, get_user, get_logged_in
from app.utils.enums import Role

view = Blueprint('doctor', __name__, url_prefix ='/')


@view.route("/doctorlk")
@role_required([Role.DOCTOR])
def lk():
    user = get_user(get_logged_in())
    doctor = get_doctor_by_id(user["doctor_id"])[0]
    plan = get_doctor_plan(doctor["id"])
    appointments = get_doctor_appointments(doctor["id"])
    for appointment in appointments:
        appointment["datetime"] = appointment["datetime"].strftime("%d.%m.%Y %H:%M:%S")
    return render_template("doctorlk.html", fio=doctor["fio"], plan=plan, appointments=appointments)


@view.route("/work")
@role_required([Role.DOCTOR])
def stats():
    return render_template("doctorfile.html")
