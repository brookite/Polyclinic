from app.api import api_blueprint
from app.db.queries import get_doctors as db_get_doctors
from flask import jsonify

@api_blueprint.route("/get_doctors")
def get_doctors():
    return jsonify(db_get_doctors())