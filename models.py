from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    def get_id(self):
           return (self.cpf_cliente)

    __tablename__ = 'cliente'
    cpf_cliente = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.Integer)
    login = db.Column(db.String(40), nullable=False, unique=True)
    senha = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
