from flask import Blueprint, render_template, request
from app.utils.login import role_required, login_required
from app.utils.enums import Role
from app.utils.login import get_logged_in
from app.db.queries import get_patient_by_id
from app.db.authorization import get_user
from app.db.queries import get_patient_appointments, get_patient_history


view = Blueprint('patient', __name__, url_prefix ='/')


@view.route("/lk")
@login_required
@role_required([Role.PATIENT])
def lk():
    patient_id = get_user(get_logged_in())["patient_id"]
    patient = get_patient_by_id(patient_id)[0]
    appointments = get_patient_appointments(patient["id"])
    for appointment in appointments:
        appointment["datetime"] = appointment["datetime"].strftime("%d.%m.%Y %H:%M:%S")
    patient["birthday"] = patient["birthday"].strftime("%d.%m.%Y")
    return render_template("lk.html", 
                           appointments=appointments,
                           fio=patient["fio"],
                           birthdate=patient["birthday"],
                           address=patient["address"],
                           phone_number=patient["phone_number"])


@view.route("/patient_file")
@login_required
@role_required([Role.PATIENT])
def patient_file():
    user = get_user(get_logged_in())
    patient = get_patient_by_id(user["patient_id"])[0]
    records = get_patient_history(patient["id"])
    for record in records:
        record["first_visit"] = record["first_visit"].strftime("%d.%m.%Y")
        if record["recovery_date"]:
            record["recovery_date"] = record["recovery_date"].strftime("%d.%m.%Y")
        else:
            record["recovery_date"] = "В процессе лечения"
    return render_template("patient_file.html", records=records)


@view.route("/appointment")
@login_required
@role_required([Role.PATIENT])
def appointment():
    user = get_user(get_logged_in())
    patient = get_patient_by_id(user["patient_id"])[0]
    return render_template(
        "appointment.html", 
        patient_name=patient["fio"], 
        patient_phone=patient["phone_number"],
        selected_doctor=request.args.get("doctor_id")
    )
