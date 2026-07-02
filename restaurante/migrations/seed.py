import sys
import os
import argparse

# Permite rodar o script de qualquer lugar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.extensions import db
from app.models import Usuario, Cliente, Funcionario, ItemCardapio


def seed(reset=False):
    app = create_app('development')

    with app.app_context():
        if reset:
            db.drop_all()
            db.create_all()
            print('Banco zerado.')
        elif Usuario.query.count() > 0:
            # Evita duplicar dados se o seed rodar mais de uma vez
            print('Banco já populado — seed ignorado. Use --reset para recriar do zero.')
            return

        # Usuários
        admin = Usuario(nome='Admin Caixa', email='admin@rest.com', papel='admin')
        admin.set_senha('admin123')

        joao = Usuario(nome='João Atendente', email='joao@rest.com', papel='atendente')
        joao.set_senha('joao123')

        maria = Usuario(nome='Maria Cliente', email='maria@rest.com', papel='cliente')
        maria.set_senha('maria123')

        db.session.add_all([admin, joao, maria])
        db.session.flush()  # gera os IDs sem commitar ainda

        # Perfis
        db.session.add(Funcionario(usuario_id=admin.id, cargo='Administrador'))
        db.session.add(Funcionario(usuario_id=joao.id,  cargo='Atendente'))
        db.session.add(Cliente(usuario_id=maria.id, telefone='(41) 99999-0001'))

        # Cardápio
        db.session.add_all([
            ItemCardapio(nome='X-Burguer',    descricao='Hambúrguer artesanal',   preco=28.90, disponivel=True),
            ItemCardapio(nome='Fritas',       descricao='Porção de batata frita', preco=15.00, disponivel=True),
            ItemCardapio(nome='Refrigerante', descricao='Lata 350ml',             preco=7.50,  disponivel=True),
            ItemCardapio(nome='Suco de Uva',  descricao='Copo 300ml',             preco=9.00,  disponivel=False),
        ])

        db.session.commit()
        print('Seed concluído com sucesso!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true',
                         help='Apaga todas as tabelas antes de popular novamente')
    args = parser.parse_args()
    seed(reset=args.reset)
