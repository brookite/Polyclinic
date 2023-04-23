from app.api import api_blueprint
from app.db.queries import get_doctors as db_get_doctors, \
     get_doctors_by_specialization as db_get_doctors_by_spec, \
     get_doctor_workshifts as db_get_doctor_workshifts
from flask import jsonify, request

@api_blueprint.route("/get_doctors")
def get_doctors():
    return jsonify(db_get_doctors())


@api_blueprint.route("/get_doctors_by_spec")
def get_doctors_by_spec():
    if spec := request.args.get("specialization"):
        return jsonify(db_get_doctors_by_spec(spec))
    else:
        return jsonify({"error_msg": "Missing 'specialization' argument"})


@api_blueprint.route("/get_doctor_workshifts")
def get_doctor_workshifts():
    if id := request.args.get("id"):
        data = db_get_doctor_workshifts(id)
        for value in data:
            value["begin_time"] = value["begin_time"].strftime("%H:%M")
            value["end_time"] = value["end_time"].strftime("%H:%M")
        return jsonify(data)
    else:
        return jsonify({"error_msg": "Missing 'specialization' argument"})