from flask import session, url_for, redirect, abort
from app.db.authorization import Role, get_user, get_roles
from typing import List



def get_logged_in():
    if session['loggedin']:
        return session["username"]


def login_required(function):
    def wrapper(*args, **kwargs):
        user = get_user(get_logged_in())
        if not user:
            return redirect(url_for('login'))
        else:
            return function(*args, **kwargs)
    
    return wrapper


def role_required(roles: List[Role]):
    def wrapper(*args, **kwargs):
        user_roles = set(get_roles(get_logged_in()).keys())
        if not len(set(roles).intersection(user_roles)):
            return "Access denied for your role", 403
        else:
            return function(*args, **kwargs)
    
    return wrapper
        