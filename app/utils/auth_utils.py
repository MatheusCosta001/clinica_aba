from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Faça login para acessar essa página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            papel = session.get("papel")
            if not papel or papel not in allowed_roles:
                flash("Permissão negada.", "danger")
                return redirect(url_for("auth.dashboard"))
            return f(*args, **kwargs)
        return wrapper
    return decorator
