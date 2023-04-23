from app.api import api_blueprint
from app.api.utils import *
from app.utils.login import role_required, get_logged_in
from app.db.authorization import get_user
from app.utils.enums import Role

from app.db.queries import create_appointment as db_create_appointment,\
    check_appointment_free

from flask import request


@api_blueprint.route("/create_appointment", methods=["POST"])
@role_required([Role.PATIENT])
def create_appointment():
    patient_id = get_user(get_logged_in())["patient_id"]
    args, missing = require_arguments(request.args, "workshift_id", "datetime")
    if not missing:
        if not len(check_appointment_free()):
            db_create_appointment(args["datetime"], args["workshift_id"], patient_id)
    else:
        return missing_arguments(missing)