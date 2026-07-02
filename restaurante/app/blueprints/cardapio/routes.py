from flask import render_template
from flask_login import login_required
from . import cardapio_bp
from app.models import ItemCardapio


@cardapio_bp.route('/')
@login_required
def index():
    itens = ItemCardapio.query.all()
    return render_template('cardapio/index.html', itens=itens)
