from flask import Blueprint, render_template, url_for


view = Blueprint('main', __name__, url_prefix ='/')


@view.route("/")
def main():
    return render_template("index.html")

@view.route("/about")
def about():
    return render_template("about.html")

@view.route("/login")
def login():
    return render_template("login.html")

@view.route("/appointment")
def appointment():
    return render_template("appoinment.html")

@view.route("/doctors")
def doctors():
    return render_template("doctors.html")