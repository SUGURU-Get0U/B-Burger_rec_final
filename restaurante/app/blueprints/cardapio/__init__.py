from flask import Blueprint

cardapio_bp = Blueprint('cardapio', __name__, url_prefix='/cardapio')

from . import routes  # noqa: E402, F401
