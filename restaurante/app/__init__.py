from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from .config import config
from .extensions import db, login_manager


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # Importa todos os modelos para o SQLAlchemy conhecer as tabelas
    from app.models import Usuario, Cliente, Funcionario  
    from app.models import ItemCardapio, Comanda, ItemComanda, Pagamento  # noqa: F401

    # Cria as tabelas no banco se ainda não existirem
    with app.app_context():
        db.create_all()

    # user_loader: Flask-Login chama isso a cada requisição para saber quem está logado
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.cardapio import cardapio_bp
    from app.blueprints.comanda import comanda_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.pagamento import pagamento_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cardapio_bp)
    app.register_blueprint(comanda_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pagamento_bp)

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('auth.dashboard'))
        return render_template('index.html')

    return app
