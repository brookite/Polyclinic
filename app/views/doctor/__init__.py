from flask import Blueprint, render_template, request
from app.db.queries import get_doctor_plan, get_doctor_appointments, \
    get_doctor_by_id, get_doctor_patient_history, get_patients, \
    get_diseases, get_medicaments, edit_patient_record, create_patient_record, \
    create_test, get_last_record_id
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


@view.route("/work", methods=["GET", "POST"])
@role_required([Role.DOCTOR])
def doctor_work():
    doctor_id = get_user(get_logged_in())["doctor_id"]
    if request.method == "POST":
        record_id = request.form["record_id"]
        if record_id:
            edit_patient_record(request.form.get("symptoms"), 
                                request.form.get("treatment_course"),
                                request.form.get("recovery_date") if request.form.get("recovery_date") else "NULL",
                                int(request.form.get("record_id"))
                                )
            #TODO: change medicaments and diseases
        else:
            create_patient_record(
                request.form.get("symptoms"), 
                request.form.get("treatment_course"),
                request.form.get("first_visit"),
                request.form.get("patient"),
                request.form.get("medicament"),
                request.form.get("disease"),
                doctor_id
            )
            record_id = get_last_record_id(request.form.get("patient"))[0]["last_record_id"]
        if request.form.get("test_name"):
            create_test(
                request.form.get("test_name"),
                request.form.get("test_datetime"),
                request.form.get("test_cost"),
                record_id
            )
    patients = get_patients()
    diseases = get_diseases()
    medicaments = get_medicaments()
    records = get_doctor_patient_history(doctor_id)
    return render_template("doctorfile.html", records=records, 
                           patients=patients, diseases=diseases, medicaments=medicaments)
