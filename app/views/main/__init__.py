from flask import Blueprint, render_template, \
    url_for, request, session, flash, redirect
from app.db.authorization import login_user, register_patient
from app.utils.login import login_required, get_logged_in, get_roles
from app.views.main.forms import LoginForm, PatientRegisterForm
from app.utils.enums import Role

from app.db.queries import get_polyclinics

view = Blueprint('main', __name__, url_prefix ='/')


@view.route("/")
def main():
    return render_template("index.html")


@view.route("/about")
def about():
    polyclinics = get_polyclinics()
    return render_template("about.html", polyclinics=polyclinics)


@view.route("/userhome")
def userhome():
    roles = get_roles(get_logged_in())
    role_names = []
    if len(roles) > 1:
        if Role.PATIENT in roles:
            role_names.append("patient")
        if Role.EMPLOYEE in roles:
            role_names.append("admin")
        if Role.DOCTOR in roles:
            role_names.append("doctor")
        print(role_names)
        return render_template("userhome.html", roles=role_names)
    elif len(roles) == 1:
        if Role.PATIENT in roles:
            return redirect(url_for('patient.lk'))
        elif Role.ADMIN in roles:
            return redirect(url_for('admin.lk'))
        elif Role.ADMIN in roles:
            return redirect(url_for('admin.admin'))
    else:
        return redirect(url_for('main.main'))


@view.route("/login", methods=['GET', 'POST'])
def login():
    if get_logged_in():
        return redirect(url_for("main.userhome"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.login.data
        password = form.password.data
        result = login_user(username, password)

        if result:
            session['loggedin'] = True
            session['id'] = result["id"]
            session['username'] = result["username"]
            return redirect(url_for('main.userhome'))
        else:
            flash('Неверное имя пользователя или пароль')
    for err in form.errors:
        flash(err)
    return render_template("login.html", form=form)


@view.route("/register", methods=['GET', 'POST'])
def register():
    required_fields = [
        "username", "password", "first_name", "middle_name", "last_name",
        "email", "phone_number", "gender",
        "address", "passport_data", "birthday"
    ]
    form = PatientRegisterForm()
    if form.validate_on_submit():
        if all(map(lambda x: x in request.form, required_fields)):
            info = dict.fromkeys(required_fields, None)
            for key in info:
                info[key] = request.form.get(key)
            result = register_patient(info)
            if result:
                return redirect(url_for('main.login'))
            else:
                flash("Проверьте правильность введенных данных")
        else:
            flash("Одно или несколько полей были не заполнены")
    for err in form.errors:
        flash(err)
    return render_template("register.html", form=form)


@view.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('main.login'))


@view.route("/doctors")
def doctors():
    return render_template("doctors.html")