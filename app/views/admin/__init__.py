from flask import Blueprint, render_template, request
from app.utils.login import role_required, get_user, get_logged_in
from app.utils.enums import Role

import datetime

from app.db.queries import get_test_cost, get_current_patient_count, \
    get_avg_recovery_time, get_disease_stats, add_new_disease, get_disease_names, \
    add_new_medicament, get_medicaments, add_doctor_office, get_doctor_offices, \
    get_diseases, add_disease_to_medicament, get_diseases, \
    get_employees, add_new_employee, edit_employee, get_doctors_full, add_new_doctor, \
    get_doctors, add_workshift

view = Blueprint('admin', __name__, url_prefix ='/')


@view.route("/stats")
@role_required([Role.EMPLOYEE])
def stats():
    total_cost = get_test_cost()[0]["cost"]
    patient_count = get_current_patient_count()[0]["patient_count"]
    avg_recovery_time = round(abs(get_avg_recovery_time()[0]["avg_recovery_time"]), 2)
    disease_stats = get_disease_stats()
    return render_template("stats.html", 
                           patient_count=patient_count,
                           total_cost=total_cost,
                           avg_recovery_time=avg_recovery_time,
                           disease_stats=disease_stats
                           )


@view.route("/admin")
@role_required([Role.EMPLOYEE])
def admin():
    return render_template("admin.html")


@view.route("/admin_workshifts", methods=["GET", "POST"])
@role_required([Role.EMPLOYEE])
def admin_workshifts():
    if request.method == "POST":
        if request.form.get("doctor"):
            add_workshift(
                request.form.get("weekday"),
                request.form.get("begin_time"),
                request.form.get("end_time"),
                request.form.get("doctor"),
                request.form.get("office")
            )
    doctors = get_doctors()
    offices = get_doctor_offices()
    return render_template("admin_workshifts.html", doctors=doctors, offices=offices)


@view.route("/admin_doctors", methods=["POST", "GET"])
@role_required([Role.EMPLOYEE])
def admin_doctors():
    if request.method == "POST":
        if request.form.get("fio"):
            add_new_doctor(
                request.form.get("fio"),
                request.form.get("specialization"),
                request.form.get("category"),
                request.form.get("passport_data"),
            )
    return render_template("admin_doctors.html", records=get_doctors_full())


@view.route("/admin_medicaments", methods=["POST", "GET"])
@role_required([Role.EMPLOYEE])
def admin_medicaments():
    if request.method == "POST":
        if request.form.get("name"):
            add_new_medicament(
                request.form.get("name"),
                request.form.get("contraindications"),
                request.form.get("indications"),
            )
        if request.form.get("disease"):
            add_disease_to_medicament(request.form.get("disease"), request.form.get("name"))

    diseases = get_diseases()
    return render_template("admin_medicaments.html", 
                           records=get_medicaments(), diseases=diseases)


@view.route("/admin_diseases", methods=["POST", "GET"])
@role_required([Role.EMPLOYEE])
def admin_diseases():
    if request.method == "POST":
        if request.form.get("disease"):
            disease = request.form.get("disease")
            add_new_disease(disease)
    return render_template("admin_diseases.html", records=get_disease_names())


@view.route("/admin_employees", methods=["POST", "GET"])
@role_required([Role.EMPLOYEE])
def admin_employees():
    if request.method == "POST":
        if request.form.get("record_id"):
            edit_employee(
                request.form.get("fio"),
                request.form.get("birthdate"),
                request.form.get("address"),
                request.form.get("passport_data"),
                request.form.get("post"),
                request.form.get("record_id")
            )
        elif request.form.get("fio"):
            add_new_employee(
                request.form.get("fio"),
                request.form.get("birthdate"),
                request.form.get("address"),
                datetime.datetime.now().date(),
                request.form.get("passport_data"),
                request.form.get("post"),
            )
    employees = get_employees()
    for employee in employees:
        employee["birthdate"] = employee["birthdate"].strftime("%Y-%m-%d")
        employee["employment_date"] = employee["employment_date"].strftime("%Y-%m-%d")
    return render_template("admin_employees.html", records=employees)


@view.route("/admin_offices", methods=["GET", "POST"])
@role_required([Role.EMPLOYEE])
def admin_offices():
    if request.method == "POST":
        if request.form.get("name"):
            add_doctor_office(
                int(request.form.get("floor")),
                request.form.get("name"),
                int(request.form.get("number")),
            )
    return render_template("admin_offices.html", records=get_doctor_offices())
