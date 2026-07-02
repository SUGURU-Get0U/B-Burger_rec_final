from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

# herda o UserMixin que fornece coisas como se o usuario esta ativo, autenticado...
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    papel      = db.Column(db.String(20),  nullable=False)  # cliente | atendente | admin
    ativo      = db.Column(db.Boolean, default=True)
    criado_em  = db.Column(db.DateTime, server_default=db.func.now())

    # Relacionamentos 1-para-1 — cascade garante que o perfil é deletado junto com o usuario
    cliente     = db.relationship('Cliente',     back_populates='usuario', uselist=False, cascade='all, delete-orphan')
    funcionario = db.relationship('Funcionario', back_populates='usuario', uselist=False, cascade='all, delete-orphan')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
