from app.api import api_blueprint
from app.utils.login import role_required, get_user, get_logged_in
from app.utils.enums import Role
from app.api.utils import *
from app.db.queries import get_doctor_patient_history, get_disease_by_name

from flask import jsonify, request

@api_blueprint.route("/get_patient_history")
@role_required([Role.DOCTOR])
def doctor_work():
    doctor_id = get_user(get_logged_in())["doctor_id"]
    patient_history = get_doctor_patient_history(doctor_id)
    for record in patient_history:
        record["first_visit"] = record["first_visit"].strftime("%Y-%m-%d")
        if record["recovery_date"]:
            record["recovery_date"] = record["recovery_date"].strftime("%Y-%m-%d")
        else:
            record["recovery_date"] = "в процессе лечения"

        if record["test_datetime"]:
            record["test_datetime"] = record["test_datetime"].strftime("%Y-%m-%d")
        else:
            record["test_datetime"] = "-"
        
        if not record["test_name"]:
            record["test_name"] = "-"
    return jsonify(patient_history)


@api_blueprint.route("/get_disease_by_name")
@role_required([Role.DOCTOR])
def get_disease():
    args, missing = require_arguments(request.args, "name")
    if not missing:
        return jsonify(get_disease_by_name(args["name"]))
    else:
        return missing_arguments(*missing)