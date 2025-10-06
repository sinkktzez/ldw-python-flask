from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Album(db.Model):
    __tablename__ = "albuns"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    fotos = db.relationship('Foto', backref='album', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Album {self.nome}>"

class Foto(db.Model):
    __tablename__ = "fotos"
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    arquivo = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    album_id = db.Column(db.Integer, db.ForeignKey('albuns.id'), nullable=False)

    def __repr__(self):
        return f"<Foto {self.titulo}>"