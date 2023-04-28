from app.api import api_blueprint
from app.api.utils import *
from app.utils.login import role_required, get_logged_in
from app.db.authorization import get_user
from app.utils.enums import Role
from datetime import datetime

from app.db.queries import create_appointment as db_create_appointment,\
    check_appointment_free

from flask import request


@api_blueprint.route("/create_appointment", methods=["POST"])
@role_required([Role.PATIENT])
def create_appointment():
    patient_id = get_user(get_logged_in())["patient_id"]
    args, missing = require_arguments(request.form, "workshift_id", "datetime")
    if not missing:
        dt = datetime.fromtimestamp(int(args["datetime"]))
        if not len(check_appointment_free(dt, int(args["workshift_id"]))):
            result = db_create_appointment(dt, int(args["workshift_id"]), patient_id)
            return jsonify(int(result))
        return jsonify(0)
    else:
        return missing_arguments(*missing)