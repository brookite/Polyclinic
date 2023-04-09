from app.api import api_blueprint
from flask import jsonify

@api_blueprint.route("/get_doctors")
def get_doctors():
    return jsonify({"test": [1, 2, 3]})