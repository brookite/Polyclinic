from app.api import api_blueprint
from app.utils.login import role_required
from app.utils.enums import Role
from app.api.utils import *

from app.db.queries import remove_doctor_office as db_remove_doctor_office
from flask import jsonify, request


@api_blueprint.route("/remove_doctor_office", methods=["GET", "POST"])
@role_required([Role.EMPLOYEE])
def remove_doctor_office():
    args, missing = require_arguments(request.args, "office_id")
    if not missing:
        return jsonify(db_remove_doctor_office(args["office_id"]))
    else:
        return missing_arguments(*missing)