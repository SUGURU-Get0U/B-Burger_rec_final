from datetime import datetime, timezone
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import comanda_bp
from app.extensions import db
from app.models import Comanda, ItemComanda, ItemCardapio


def _get_comanda_ou_403(id):
    comanda = Comanda.query.get(id)
    if not comanda:
        flash('Comanda não encontrada.', 'erro')
        return None, redirect(url_for('comanda.index'))

    # Cliente só acessa a própria comanda — compara pelo perfil Cliente, não pelo Usuario
    if current_user.papel == 'cliente':
        perfil = current_user.cliente
        if not perfil or comanda.cliente_id != perfil.id:
            flash('Acesso negado.', 'erro')
            return None, redirect(url_for('comanda.index'))

    return comanda, None


# --- Listagem ---

@comanda_bp.route('/')
@login_required
def index():
    if current_user.papel == 'cliente' and current_user.cliente:
        comandas = Comanda.query.filter_by(cliente_id=current_user.cliente.id).all()
    else:
        comandas = Comanda.query.all()
    return render_template('comanda/index.html', comandas=comandas)


# --- Criar comanda ---

@comanda_bp.route('/nova', methods=['POST'])
@login_required
def nova():
    cliente_id = None
    if current_user.papel == 'cliente' and current_user.cliente:
        cliente_id = current_user.cliente.id

    comanda = Comanda(estado='aberta', cliente_id=cliente_id, codigo=0)
    db.session.add(comanda)
    db.session.flush()          # gera o id sem commitar
    comanda.codigo = comanda.id  # codigo == id no RA3
    db.session.commit()

    flash(f'Comanda #{comanda.codigo} criada!', 'sucesso')
    return redirect(url_for('comanda.detalhe', id=comanda.id))


# --- Detalhe da comanda ---

@comanda_bp.route('/<int:id>')
@login_required
def detalhe(id):
    comanda, erro = _get_comanda_ou_403(id)
    if erro:
        return erro
    itens_cardapio = ItemCardapio.query.all()
    return render_template('comanda/detalhe.html', comanda=comanda, itens_cardapio=itens_cardapio)


# --- Adicionar item ---

@comanda_bp.route('/<int:id>/adicionar', methods=['POST'])
@login_required
def adicionar_item(id):
    comanda, erro = _get_comanda_ou_403(id)
    if erro:
        return erro

    if comanda.estado == 'paga':
        flash('Comanda já paga não pode ser editada.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    if comanda.estado == 'fechada' and current_user.papel != 'admin':
        flash('Apenas administradores podem editar comanda fechada.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    item = ItemCardapio.query.get(request.form.get('item_id', 0))
    if not item or not item.disponivel:
        flash('Item indisponível ou inválido.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    try:
        quantidade = int(request.form.get('quantidade', 0))
    except ValueError:
        quantidade = 0

    if quantidade <= 0:
        flash('Quantidade deve ser maior que zero.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    # Se o item já existe na comanda, incrementa a quantidade
    existente = next((i for i in comanda.itens if i.item_cardapio_id == item.id), None)
    if existente:
        existente.quantidade += quantidade
        existente.subtotal    = existente.preco_unitario * existente.quantidade
        db.session.commit()
        flash(f'{item.nome} atualizado na comanda.', 'sucesso')
        return redirect(url_for('comanda.detalhe', id=id))

    novo_item = ItemComanda(
        comanda_id       = comanda.id,
        item_cardapio_id = item.id,
        quantidade       = quantidade,
        preco_unitario   = item.preco,   # snapshot do preco atual
        subtotal         = item.preco * quantidade,
    )
    db.session.add(novo_item)
    db.session.commit()
    flash(f'{item.nome} adicionado à comanda.', 'sucesso')
    return redirect(url_for('comanda.detalhe', id=id))


# --- Remover item ---

@comanda_bp.route('/<int:id>/remover/<int:item_cardapio_id>', methods=['POST'])
@login_required
def remover_item(id, item_cardapio_id):
    comanda, erro = _get_comanda_ou_403(id)
    if erro:
        return erro

    if comanda.estado == 'paga':
        flash('Comanda já paga não pode ser editada.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    if comanda.estado == 'fechada' and current_user.papel != 'admin':
        flash('Apenas administradores podem editar comanda fechada.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    item = next((i for i in comanda.itens if i.item_cardapio_id == item_cardapio_id), None)
    if item:
        db.session.delete(item)
        db.session.commit()
    flash('Item removido.', 'sucesso')
    return redirect(url_for('comanda.detalhe', id=id))


# --- Fechar comanda ---

@comanda_bp.route('/<int:id>/fechar', methods=['POST'])
@login_required
def fechar(id):
    if current_user.papel == 'cliente':
        flash('Apenas atendentes podem fechar comandas.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    comanda, erro = _get_comanda_ou_403(id)
    if erro:
        return erro

    if comanda.estado != 'aberta':
        flash('Comanda já está fechada ou paga.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    if not comanda.itens:
        flash('Não é possível fechar uma comanda sem itens.', 'erro')
        return redirect(url_for('comanda.detalhe', id=id))

    comanda.estado         = 'fechada'
    comanda.fechado_em     = datetime.now(timezone.utc)
    comanda.fechado_por_id = current_user.id   # auditoria
    db.session.commit()

    flash(f'Comanda #{comanda.codigo} fechada com sucesso.', 'sucesso')
    return redirect(url_for('comanda.detalhe', id=id))
