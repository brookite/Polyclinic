from app.api import api_blueprint
from app.utils.login import role_required
from app.utils.enums import Role
from app.api.utils import *

from app.db.queries import remove_doctor_office as db_remove_doctor_office, \
    get_employees as db_get_employees, get_doctors_full as db_get_doctors, \
    remove_doctor as db_remove_doctor
from flask import jsonify, request


@api_blueprint.route("/remove_doctor_office", methods=["GET", "POST"])
@role_required([Role.EMPLOYEE])
def remove_doctor_office():
    args, missing = require_arguments(request.args, "office_id")
    if not missing:
        return jsonify(db_remove_doctor_office(args["office_id"]))
    else:
        return missing_arguments(*missing)



@api_blueprint.route("/get_employees")
@role_required([Role.EMPLOYEE])
def get_employees():
    employees = db_get_employees()
    for employee in employees:
        employee["birthdate"] = employee["birthdate"].strftime("%Y-%m-%d")
        employee["employment_date"] = employee["employment_date"].strftime("%Y-%m-%d")
    return jsonify(employees)


@api_blueprint.route("/get_doctors_full")
@role_required([Role.EMPLOYEE])
def get_doctors_full():
    doctors = db_get_doctors()
    return jsonify(doctors)


@api_blueprint.route("/remove_doctor")
@role_required([Role.EMPLOYEE])
def remove_doctor():
    args, missing = require_arguments(request.args, "id")
    if not missing:
        return jsonify(db_remove_doctor(*[args["id"] for i in range(5)]))
    else:
        return missing_arguments(*missing)
