from app.extensions import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id         = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    telefone   = db.Column(db.String(20), nullable=True)
    criado_em  = db.Column(db.DateTime, server_default=db.func.now())

    # Navegação para o Usuario dono deste perfil
    usuario  = db.relationship('Usuario', back_populates='cliente')

    # Um cliente pode ter várias comandas
    comandas = db.relationship('Comanda', back_populates='cliente')
