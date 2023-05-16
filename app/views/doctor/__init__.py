from flask import Blueprint, render_template, request
from app.db.queries import get_doctor_plan, get_doctor_appointments, \
    get_doctor_by_id, get_doctor_patient_history, get_patients, \
    get_diseases, get_medicaments, edit_patient_record, create_patient_record, \
    create_test, get_last_record_id, remove_diseases_for_record, remove_medicaments_for_record, \
    add_disease_to_record, add_medicament_to_record, get_disease_by_name

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
    patients = get_patients()
    diseases = get_diseases()
    medicaments = get_medicaments()
    if request.method == "POST":
        record_id = request.form["record_id"]
        if record_id:
            edit_patient_record(request.form.get("symptoms"), 
                                request.form.get("treatment_course"),
                                request.form.get("recovery_date") if request.form.get("recovery_date") else None,
                                int(request.form.get("record_id"))
                                )
        else:
            create_patient_record(
                request.form.get("symptoms"), 
                request.form.get("treatment_course"),
                request.form.get("first_visit"),
                request.form.get("patient"),
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
        disease_list = request.form.get("diseases", "").split(",")
        medicament_list = request.form.get("medicaments", "").split(",")
        remove_diseases_for_record(record_id)
        remove_medicaments_for_record(record_id)
        for disease in disease_list:
            d_id = get_disease_by_name(disease)
            if len(d_id):
                d_id = d_id[0]["id"]
                add_disease_to_record(record_id, d_id)
        for medicament in medicament_list:
            add_medicament_to_record(record_id, medicament)
    records = get_doctor_patient_history(doctor_id)
    for record in records:
        for key in record:
            if record[key] is None:
                record[key] = "-"
        if not isinstance(record["test_datetime"], str):
            record["test_datetime"] = record["test_datetime"].strftime("%d.%m.%Y %H:%M:%S")
    return render_template("doctorfile.html", records=records, 
                           patients=patients, diseases=diseases, medicaments=medicaments)
