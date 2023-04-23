from app.api import api_blueprint
from app.api.utils import *
from app.db.queries import get_doctors as db_get_doctors, \
     get_doctors_by_specialization as db_get_doctors_by_spec, \
     get_doctor_workshifts as db_get_doctor_workshifts, \
     get_appointments_at_workshift as db_get_appointments_at_workshift
from flask import jsonify, request



@api_blueprint.route("/get_doctors")
def get_doctors():
    return jsonify(db_get_doctors())


@api_blueprint.route("/get_doctors_by_spec")
def get_doctors_by_spec():
    args, missing = require_arguments(request.args, "specialization")
    if not missing:
        return jsonify(db_get_doctors_by_spec(args["specialization"]))
    else:
        return missing_arguments(missing)


@api_blueprint.route("/get_doctor_workshifts")
def get_doctor_workshifts():
    args, missing = require_arguments(request.args, "id")
    if not missing:
        data = db_get_doctor_workshifts(args["id"])
        for value in data:
            value["begin_time"] = value["begin_time"].strftime("%H:%M")
            value["end_time"] = value["end_time"].strftime("%H:%M")
        return jsonify(data)
    else:
        return missing_arguments("id")


@api_blueprint.route("/get_workshift_appointments")
def get_workshift_appointments():
    args, missing = require_arguments(request.args, "workshift_id")
    if not missing:
        return jsonify(db_get_appointments_at_workshift(args["workshift_id"]))
    else:
        return missing_arguments("workshift_id")



