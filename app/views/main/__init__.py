from flask import Blueprint, render_template, \
    url_for, request, session, flash, redirect
from app.db.authorization import login_user, register_patient
from app.utils.enums import Role
from app.utils.login import login_required, role_required

view = Blueprint('main', __name__, url_prefix ='/')


@view.route("/")
def main():
    return render_template("index.html")


@view.route("/about")
def about():
    return render_template("about.html")


@view.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' \
         and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        result = login_user(username, password)

        if result:
            session['loggedin'] = True
            session['id'] = result["id"]
            session['username'] = result["username"]
            return redirect(url_for('/userhome'))
        else:
            flash('Incorrect username/password')

    return render_template("login.html")


@view.route("/register", methods=['GET', 'POST'])
def register():
    required_fields = [
        "username", "password", "first_name", "middle_name", "last_name",
        "email", "phone_number", "gender",
        "address", "passport_data", "birthday"
    ]
    if request.method == 'POST':
        if all(map(lambda x: x in request.form, required_fields)):
            info = dict.fromkeys(required_fields, None)
            for key in info:
                info[key] = request.form.get(key)
            # TODO: add data validation
            result = register_patient(info)
        else:
            pass
    return render_template("register.html")


@login_required
@view.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('/login'))


@role_required([Role.PATIENT])
@view.route("/appointment")
def appointment():
    return render_template("appointment.html")


@view.route("/doctors")
def doctors():
    return render_template("doctors.html")