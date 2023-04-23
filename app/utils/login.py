from flask import session, url_for, redirect, abort
from app.db.authorization import Role, get_user, get_roles
from typing import List
from functools import wraps


def get_logged_in():
    if session.get('loggedin'):
        return session["username"]


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = get_user(get_logged_in())
        if not user:
            return redirect(url_for('main.login'))
        else:
            return function(*args, **kwargs)
    
    return wrapper


def role_required(roles: List[Role]):
    def role_wrapper(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user_roles = set(get_roles(get_logged_in()).keys())
            if not len(set(roles).intersection(user_roles)):
                return "Доступ к данной странице запрещен для этой роли пользователя", 403
            else:
                return function(*args, **kwargs)
        return wrapper
    
    return role_wrapper
        