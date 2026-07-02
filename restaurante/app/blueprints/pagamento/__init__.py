from flask import Blueprint

pagamento_bp = Blueprint('pagamento', __name__, url_prefix='/pagamento')

from . import routes  # noqa: E402, F401
