from app.extensions import db


class Comanda(db.Model):
    __tablename__ = 'comandas'

    id             = db.Column(db.Integer, primary_key=True)
    codigo         = db.Column(db.Integer, nullable=False, unique=True)
    estado         = db.Column(db.String(10), nullable=False, default='aberta')  # aberta|fechada|paga
    cliente_id     = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    criado_em      = db.Column(db.DateTime, server_default=db.func.now())
    fechado_em     = db.Column(db.DateTime, nullable=True)
    fechado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    pago_em        = db.Column(db.DateTime, nullable=True)
    pago_por_id    = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    # Relacionamentos
    cliente     = db.relationship('Cliente',  back_populates='comandas',
                                  foreign_keys=[cliente_id])
    fechado_por = db.relationship('Usuario',  foreign_keys=[fechado_por_id])
    pago_por    = db.relationship('Usuario',  foreign_keys=[pago_por_id])
    itens       = db.relationship('ItemComanda', back_populates='comanda',
                                  cascade='all, delete-orphan')
    pagamento   = db.relationship('Pagamento', back_populates='comanda', uselist=False)

    @property
    def total(self):
        return sum(i.subtotal for i in self.itens)
