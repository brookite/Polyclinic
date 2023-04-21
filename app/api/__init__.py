from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix ='/api')

import app.api.admin as admin
import app.api.patient as patient
import app.api.common as common
import app.api.doctor as doctor