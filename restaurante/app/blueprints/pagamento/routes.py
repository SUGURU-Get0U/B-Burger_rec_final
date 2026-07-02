from datetime import datetime, timezone
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import pagamento_bp
from app.extensions import db
from app.models import Comanda, Pagamento
from app.decorators import admin_required


@pagamento_bp.route('/<int:comanda_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def liquidar(comanda_id):
    comanda = Comanda.query.get(comanda_id)

    if not comanda:
        flash('Comanda não encontrada.', 'erro')
        return redirect(url_for('comanda.index'))

    if comanda.estado != 'fechada':
        flash('Apenas comanda fechada pode ser liquidada.', 'erro')
        return redirect(url_for('comanda.detalhe', id=comanda_id))

    if request.method == 'POST':
        forma    = request.form.get('forma_pagamento', '').strip()
        try:
            recebido = float(request.form.get('valor_recebido', 0))
        except ValueError:
            recebido = 0.0

        total = float(comanda.total)

        if not forma:
            flash('Informe a forma de pagamento.', 'erro')
        elif recebido < total:
            flash(f'Valor recebido (R$ {recebido:.2f}) menor que o total (R$ {total:.2f}).', 'erro')
        else:
            troco = recebido - total

            pagamento = Pagamento(
                comanda_id      = comanda.id,
                forma_pagamento = forma,
                valor_recebido  = recebido,
                troco           = troco,
                registrado_por  = current_user.id,
            )
            db.session.add(pagamento)

            comanda.estado      = 'paga'
            comanda.pago_em     = datetime.now(timezone.utc)
            comanda.pago_por_id = current_user.id   # auditoria

            db.session.commit()
            return redirect(url_for('pagamento.comprovante', comanda_id=comanda.id))

    return render_template('pagamento/liquidar.html', comanda=comanda)


@pagamento_bp.route('/<int:comanda_id>/comprovante')
@login_required
def comprovante(comanda_id):
    comanda = Comanda.query.get(comanda_id)
    if not comanda or comanda.estado != 'paga':
        flash('Comprovante indisponível.', 'erro')
        return redirect(url_for('comanda.index'))
    return render_template('pagamento/comprovante.html', comanda=comanda)
