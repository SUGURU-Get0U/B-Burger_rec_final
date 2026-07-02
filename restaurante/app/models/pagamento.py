from app.extensions import db


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id               = db.Column(db.Integer, primary_key=True)
    comanda_id       = db.Column(db.Integer, db.ForeignKey('comandas.id'), unique=True, nullable=False)
    forma_pagamento  = db.Column(db.String(30), nullable=False)  # dinheiro | cartão | pix
    valor_recebido   = db.Column(db.Numeric(10, 2), nullable=False)
    troco            = db.Column(db.Numeric(10, 2), nullable=False)
    registrado_por   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    registrado_em    = db.Column(db.DateTime, server_default=db.func.now())

    # Relacionamentos
    comanda           = db.relationship('Comanda',  back_populates='pagamento')
    usuario_registrou = db.relationship('Usuario',  foreign_keys=[registrado_por])
