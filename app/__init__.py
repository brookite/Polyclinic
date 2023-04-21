from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path="/")

    import app.views.main as main
    import app.views.admin as admin
    import app.views.patient as patient
    import app.views.doctor as doctor

    import app.api as api

    app.register_blueprint(main.view)
    app.register_blueprint(admin.view)
    app.register_blueprint(patient.view)
    app.register_blueprint(doctor.view)
    app.register_blueprint(api.api_blueprint)

    return app