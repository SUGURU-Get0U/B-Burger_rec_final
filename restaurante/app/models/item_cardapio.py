from app.extensions import db


class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'

    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100), nullable=False)
    descricao  = db.Column(db.Text, nullable=True)
    preco      = db.Column(db.Numeric(10, 2), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    criado_em  = db.Column(db.DateTime, server_default=db.func.now())

    # Um item pode aparecer em várias comandas
    itens_comanda = db.relationship('ItemComanda', back_populates='item_cardapio')
