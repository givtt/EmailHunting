from ..app import EmailServer
from functools import wraps
from flask import redirect, url_for


def is_user_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        app = EmailServer

        if app.is_login():
            return func(*args, **kwargs)
        else:
            if app.re_login():
                return decorated_function(*args, **kwargs)
            else:
                # If re-login fails, redirect to login page
                return redirect(url_for("auth.login"))
    return decorated_function
