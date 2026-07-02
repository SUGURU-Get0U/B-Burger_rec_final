from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.papel != 'admin':
            flash('Acesso restrito a administradores.', 'erro')
            return redirect(url_for('auth.dashboard'))
        return f(*args, **kwargs)
    return decorated
