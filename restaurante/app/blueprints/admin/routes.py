from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import admin_bp
from app.decorators import admin_required
from app.extensions import db
from app.models import Usuario, Cliente, Funcionario, ItemCardapio, ItemComanda


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

@admin_bp.route('/clientes')
@login_required
@admin_required
def clientes():
    lista = Usuario.query.filter_by(papel='cliente').all()
    return render_template('admin/clientes.html', clientes=lista)


@admin_bp.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_cliente():
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'erro')
        elif Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'erro')
        else:
            usuario = Usuario(nome=nome, email=email, papel='cliente')
            usuario.set_senha(senha)
            db.session.add(usuario)
            db.session.flush()
            db.session.add(Cliente(usuario_id=usuario.id))
            db.session.commit()
            flash('Cliente criado com sucesso.', 'sucesso')
            return redirect(url_for('admin.clientes'))
    return render_template('admin/form_usuario.html', titulo='Novo Cliente',
                           action=url_for('admin.novo_cliente'))


@admin_bp.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_cliente(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Cliente não encontrado.', 'erro')
        return redirect(url_for('admin.clientes'))
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        if not nome or not email:
            flash('Preencha todos os campos.', 'erro')
        else:
            usuario.nome  = nome
            usuario.email = email
            db.session.commit()
            flash('Cliente atualizado.', 'sucesso')
            return redirect(url_for('admin.clientes'))
    return render_template('admin/form_usuario.html', titulo='Editar Cliente',
                           action=url_for('admin.editar_cliente', id=id), usuario=usuario)


@admin_bp.route('/clientes/<int:id>/remover', methods=['POST'])
@login_required
@admin_required
def remover_cliente(id):
    if id == current_user.id:
        flash('Você não pode remover sua própria conta.', 'erro')
        return redirect(url_for('admin.clientes'))
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    flash('Cliente removido.', 'sucesso')
    return redirect(url_for('admin.clientes'))


# ---------------------------------------------------------------------------
# Funcionários
# ---------------------------------------------------------------------------

@admin_bp.route('/funcionarios')
@login_required
@admin_required
def funcionarios():
    lista = Usuario.query.filter(Usuario.papel.in_(['atendente', 'admin'])).all()
    return render_template('admin/funcionarios.html', funcionarios=lista)


@admin_bp.route('/funcionarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_funcionario():
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        papel = request.form.get('papel', 'atendente')
        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'erro')
        elif Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'erro')
        else:
            usuario = Usuario(nome=nome, email=email, papel=papel)
            usuario.set_senha(senha)
            db.session.add(usuario)
            db.session.flush()
            db.session.add(Funcionario(usuario_id=usuario.id, cargo=papel.capitalize()))
            db.session.commit()
            flash('Funcionário criado com sucesso.', 'sucesso')
            return redirect(url_for('admin.funcionarios'))
    return render_template('admin/form_funcionario.html', titulo='Novo Funcionário',
                           action=url_for('admin.novo_funcionario'))


@admin_bp.route('/funcionarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_funcionario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Funcionário não encontrado.', 'erro')
        return redirect(url_for('admin.funcionarios'))
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        if not nome or not email:
            flash('Preencha todos os campos.', 'erro')
        else:
            usuario.nome  = nome
            usuario.email = email
            db.session.commit()
            flash('Funcionário atualizado.', 'sucesso')
            return redirect(url_for('admin.funcionarios'))
    return render_template('admin/form_funcionario.html', titulo='Editar Funcionário',
                           action=url_for('admin.editar_funcionario', id=id), usuario=usuario)


@admin_bp.route('/funcionarios/<int:id>/remover', methods=['POST'])
@login_required
@admin_required
def remover_funcionario(id):
    if id == current_user.id:
        flash('Você não pode remover sua própria conta.', 'erro')
        return redirect(url_for('admin.funcionarios'))
    total_admins = Usuario.query.filter_by(papel='admin').count()
    usuario = Usuario.query.get(id)
    if usuario and usuario.papel == 'admin' and total_admins <= 1:
        flash('Não é possível remover o único administrador do sistema.', 'erro')
        return redirect(url_for('admin.funcionarios'))
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    flash('Funcionário removido.', 'sucesso')
    return redirect(url_for('admin.funcionarios'))


# ---------------------------------------------------------------------------
# Cardápio
# ---------------------------------------------------------------------------

@admin_bp.route('/cardapio')
@login_required
@admin_required
def cardapio():
    return render_template('admin/cardapio.html', itens=ItemCardapio.query.all())


@admin_bp.route('/cardapio/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_item():
    if request.method == 'POST':
        nome       = request.form.get('nome', '').strip()
        descricao  = request.form.get('descricao', '').strip()
        preco      = request.form.get('preco', '')
        disponivel = request.form.get('disponivel') == 'on'
        if not nome or not preco:
            flash('Nome e preço são obrigatórios.', 'erro')
        else:
            db.session.add(ItemCardapio(nome=nome, descricao=descricao,
                                        preco=preco, disponivel=disponivel))
            db.session.commit()
            flash('Item criado com sucesso.', 'sucesso')
            return redirect(url_for('admin.cardapio'))
    return render_template('admin/form_item.html', titulo='Novo Item',
                           action=url_for('admin.novo_item'))


@admin_bp.route('/cardapio/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_item_cardapio(id):
    item = ItemCardapio.query.get(id)
    if not item:
        flash('Item não encontrado.', 'erro')
        return redirect(url_for('admin.cardapio'))
    if request.method == 'POST':
        nome       = request.form.get('nome', '').strip()
        descricao  = request.form.get('descricao', '').strip()
        preco      = request.form.get('preco', '')
        disponivel = request.form.get('disponivel') == 'on'
        if not nome or not preco:
            flash('Nome e preço são obrigatórios.', 'erro')
        else:
            item.nome       = nome
            item.descricao  = descricao
            item.preco      = preco
            item.disponivel = disponivel
            db.session.commit()
            flash('Item atualizado.', 'sucesso')
            return redirect(url_for('admin.cardapio'))
    return render_template('admin/form_item.html', titulo='Editar Item',
                           action=url_for('admin.editar_item_cardapio', id=id), item=item)


@admin_bp.route('/cardapio/<int:id>/remover', methods=['POST'])
@login_required
@admin_required
def remover_item_cardapio(id):
    item = ItemCardapio.query.get(id)
    if not item:
        flash('Item não encontrado.', 'erro')
        return redirect(url_for('admin.cardapio'))

    em_uso = ItemComanda.query.filter_by(item_cardapio_id=id).first()
    if em_uso:
        flash(f'"{item.nome}" não pode ser removido pois está em comandas existentes. '
              'Desative a disponibilidade em vez de remover.', 'erro')
        return redirect(url_for('admin.cardapio'))

    db.session.delete(item)
    db.session.commit()
    flash('Item removido.', 'sucesso')
    return redirect(url_for('admin.cardapio'))
