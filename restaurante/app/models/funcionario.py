from app.extensions import db


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id         = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    cargo      = db.Column(db.String(50), nullable=False)
    criado_em  = db.Column(db.DateTime, server_default=db.func.now())

    # Navegação para o Usuario dono deste perfil
    usuario = db.relationship('Usuario', back_populates='funcionario')
