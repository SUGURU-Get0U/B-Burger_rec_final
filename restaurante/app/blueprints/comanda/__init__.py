from flask import Blueprint

comanda_bp = Blueprint('comanda', __name__, url_prefix='/comanda')

from . import routes  # noqa: E402, F401
