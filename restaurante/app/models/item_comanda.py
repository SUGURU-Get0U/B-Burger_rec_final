from app.extensions import db


class ItemComanda(db.Model):
    __tablename__ = 'itens_comanda'

    id                = db.Column(db.Integer, primary_key=True)
    comanda_id        = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False)
    item_cardapio_id  = db.Column(db.Integer, db.ForeignKey('itens_cardapio.id'), nullable=False)
    quantidade        = db.Column(db.Integer, nullable=False)
    preco_unitario    = db.Column(db.Numeric(10, 2), nullable=False)  # snapshot do momento
    subtotal          = db.Column(db.Numeric(10, 2), nullable=False)

    # Relacionamentos
    comanda       = db.relationship('Comanda',      back_populates='itens')
    item_cardapio = db.relationship('ItemCardapio', back_populates='itens_comanda')
