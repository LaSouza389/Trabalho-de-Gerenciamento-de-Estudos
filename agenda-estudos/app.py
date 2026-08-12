# BIBLIOTECAS
from flask import Flask, render_template, request, redirect, url_for # Importação Do flask
from flask_sqlalchemy import SQLAlchemy # Importação do SQLAlchemy para o DB
from sqlalchemy import Column, Integer, String # Importação de algumas funcionalidades do DB
from werkzeug.security import generate_password_hash , check_password_hash

# SESSAO Q CRIA A INSTANCIA PRINCIPAL DO FLASK
app = Flask(__name__)

# CONFIGURA COMO Q O FLASK VAI SE CONECTAR AO DB COM O SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agenda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# INICIALIZA O SQLAalchemy DENTRO DA MINHA APLICAÇÃO FLASK
db = SQLAlchemy(app)

# CRIAÇÃO DA TABELA DE USUARIOS E DAS COLUNAS INTERNAS (a id ,nome, email e senha )
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha =  db.Column(db.String(200), nullable=False)

# CRIANDO O BANCO DE DADOS
with app.app_context():
    db.create_all()

# CRIAÇÃO DA ROTA DE CADASTRO
@app.route("/cadastro", methods = ["GET" , "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Encryptando..
        senha_hash = generate_password_hash(senha)

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash
        )
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("cadastro.html")

# CRIAÇÃO DA ROTA DE LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        # VERIFICA NO DB DE UM USER SE TEM OS MSM (Usuario,email)
        usuario = Usuario.query.filter_by(email=email).first() 

        if usuario and check_password_hash(usuario.senha, senha):
            return redirect(url_for("agenda"))

        return "Email ou senha incorretos"
    
    return render_template("login.html")

# ROTA DA AGENDA 
@app.route("/agenda") 
def agenda():
    