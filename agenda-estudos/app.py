# BIBLIOTECAS
from flask import Flask, render_template, request, redirect, url_for, session # Importação Do flask
from flask_sqlalchemy import SQLAlchemy # Importação do SQLAlchemy para o DB
from sqlalchemy import Column, Integer, String # Importação de algumas funcionalidades do DB
from werkzeug.security import generate_password_hash , check_password_hash
from datetime import date

# SESSAO Q CRIA A INSTANCIA PRINCIPAL DO FLASK
app = Flask(__name__)
app.config["SECRET_KEY"] = "fjdfnljfkmefiweyefyrioyojkfmdjrji"

# CONFIGURA COMO Q O FLASK VAI SE CONECTAR AO DB COM O SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agenda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# INICIALIZA O SQLAalchemy DENTRO DA MINHA APLICAÇÃO FLASK
db = SQLAlchemy(app) 

# CRIAÇÃO DA TABELA DE USUARIOS E AS COLUNAS INTERNAS (a id ,nome, email e senha )
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha =  db.Column(db.String(200), nullable=False)

# CRIAÇÃO DA TABELA ESTUDO E AS COLUNAS INTERNAS 
class Estudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    data = db.Column(db.String(20))
    concluido = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, nullable=True)


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


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        # VERIFICA NO DB DE UM USER SE TEM OS MSM (Usuario,email)
        usuario = Usuario.query.filter_by(email=email).first() 

        if usuario and check_password_hash(usuario.senha, senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome

            return redirect(url_for("agenda"))

        return "Email ou senha incorretos"
    
    return render_template("login.html")


@app.route("/agenda")
def agenda():

    filtro = request.args.get("filtro", "todos")

    usuario_id = session["usuario_id"]

    if filtro == "pendentes":
        estudos = Estudo.query.filter_by(
            usuario_id=usuario_id,
            concluido=False
        ).all()

    elif filtro == "concluidos":
        estudos = Estudo.query.filter_by(
            usuario_id=usuario_id,
            concluido=True
        ).all()

    else:
        estudos = Estudo.query.filter_by(
            usuario_id=usuario_id
        ).all()

    # Verifica quais estudos estão atrasados
    for estudo in estudos:

        if estudo.data and estudo.data != "Sem data final":

            data_entrega = date.fromisoformat(estudo.data)

            if data_entrega < date.today() and not estudo.concluido:
                estudo.atrasado = True
            else:
                estudo.atrasado = False

        else:
            estudo.atrasado = False

    usuario = Usuario.query.get(session["usuario_id"])

    return render_template(
        "agenda.html",
        estudos=estudos,
        usuario=usuario
    )

@app.route("/adicionar_estudo", methods=["POST"])
def adicionar_estudo():

    materia = request.form["materia"]
    descricao = request.form["descricao"]
    data = request.form.get("data")

    if not data:
        data = "Sem data final"

    usuario_id = session["usuario_id"]

    estudo = Estudo(
        materia=materia,
        descricao=descricao,
        data=data,
        usuario_id=usuario_id
    )

    db.session.add(estudo)
    db.session.commit()

    return redirect(url_for("agenda"))

@app.route("/concluir_estudo/<int:id>", methods=["POST"])
def concluir_estudo(id):

    estudo = Estudo.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if estudo:
        estudo.concluido = True
        db.session.commit()

    return redirect(url_for("agenda"))


@app.route("/excluir_estudo/<int:id>", methods=["POST"])
def excluir_estudo(id):

    estudo = Estudo.query.filter_by (
        id=id,
        usuario_id=session["usuario_id"]
        ).first()

    if estudo:
        db.session.delete(estudo)
        db.session.commit()

    return redirect(url_for("agenda"))


# CRIANDO O BANCO DE DADOS
with app.app_context():
    db.create_all()

# EXECUTA TUDO 
print(app.url_map)
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True) # TIVE Q ESCREVER MANUALMENTE PQ TAVA DANDO BUGS

  