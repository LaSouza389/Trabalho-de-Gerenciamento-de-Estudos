# BIBLIOTECAS
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

# SESSAO Q CRIA A INSTANCIA PRINCIPAL DO FLASK
app = Flask(__name__)

# CONFIGURA COMO Q O FLASK VAI SE CONECTAR AO DB COM O SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agenda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# INICIALIZA O SQLAalchemy DENTRO DA MINHA APLICAÇÃO FLASK
db = SQLAlchemy(app)

# CRIAÇÃO DA TABELA DE USUARIOS E DAS COLUNAS INTERNAS (a id ,nome, email e senha )
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Colum(db.String(100), unique = True, nullable = False)
    senha =  db.Column(db.String(200), nullable = False)

# CRIANDO O BANCO DE DADOS
with app.app_context():
    db.create_all()
    