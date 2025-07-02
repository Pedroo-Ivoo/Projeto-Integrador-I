from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy

#todo Aprender btcrypt ou algo assim para o login ser seguro.

#Conecta com o banco de dados que já foi criado anteriormente.
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"database.db"))

app = Flask(__name__)
app.secret_key = 'temosUmaChaveAqui102' #chave secreta faz com o cookie salve as informações que só podem ser acessadas por quem tem a chave.
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# Função que verifica se está logado para o acesso as páginas Será chamada nas rotas
def verifica_login():
    if not session.get("usuario_logado", False):
        return redirect(url_for("login")) #Redireciona para a rota do login
        
#classe correspondente as tabelas.
class Regioes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    #Estabelece a relação entre as tabelas Motoristas e Alunos
    motoristas = db.relationship("Motoristas", backref="regiao", lazy=True)
    alunos = db.relationship("Alunos", backref="regiao", lazy=True)

class Motoristas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    rota = db.Column(db.String(50), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    regiao_id = db.Column(db.Integer, db.ForeignKey('regioes.id'), nullable=False)  # Chave estrangeira

    
class Alunos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    motorista_id = db.Column(db.Integer,db.ForeignKey("motorista_id"), nullable=False)
    regiao_id = db.Column(db.Integer, db.ForeignKey('regioes.id'), nullable=False)  # Chave estrangeira
    motorista_id = db.Column(db.Integer, db.ForeignKey('motoristas.id'))
    motorista = db.relationship('Motoristas', backref='alunos')

    



# Cria a rota da página inicial, quando o navegador recebe o endereço da página inicial ele apresentará a página index.
@app.route("/")
def index():
    return render_template('index.html')

# Rota para a página login
# Aqui o parâmetro que rota recebe veio de um a href do html por ser uma simples requisição.
@app.route("/login")
def acesso():
    return render_template("login.html")

#Verificação de autenticação
@app.route("/login", methods=["POST"])
def login():

    if request.method == "POST":
        
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
    
        #Controle de acesso.
        if usuario == "Administrador" and senha == "admin":
            session['usuario_logado'] = True 
            session['nome'] = usuario
            return redirect(url_for("home"))
        else:
            erro = "Usuário ou senha inválidos!"
            return render_template('login.html', erro=erro) 
    return render_template('login.html') 

#Rota para a página home
@app.route("/home")
def home():
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login
    nome = f"Bem vindo, {session['nome']}"
    return render_template("home.html", nome=nome)      

#Rota para o logout do sistema
@app.route("/logout")
def logout():
    session.pop('usuario_logado', None)
    session.pop('nome', None)
    return redirect(url_for("index"))

# Rota que realiza o cadastro dos motoristas
@app.route("/cadastro_motoristas", methods={"GET", "POST"})
#No inicio da função verifica se o usuário está logado na página.
#Estando logado passa para a parte que realiza o cadastro de novos motoristas para o banco de dados.

def cadastro_motoristas():
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login

    if request.method == "POST":
        #As variaveis vem do formulário na página html
        nome = request.form.get("nome", "").upper().strip() #Upper deixa todos os caracteres em maiuscula e o strip remove os espaços em branco no início ou no final do input
        rota = request.form.get("rota", "").upper().strip()
        celular = request.form.get("celular")
        regiao_id = request.form.get("regiao_id")  # Obtendo a ID da região selecionada
        cadastro_existente = Motoristas.query.filter_by(nome=nome).first() #realiza a consulta no banco.
        #Verifica se o nome cadastrado já se encontra no banco de dados, se já constar retornará um aviso ao usuário
        if cadastro_existente:
            flash(f"Nome já consta cadastrado, verifique em exibir cadastro.")
            return render_template("cadastro_motoristas.html")
        #Verifica se os dados do formulário forma preenchidos. Caso algum esteja em branco retorna o aviso ao usuário.
        if not nome or not rota or not regiao_id or not celular:
            flash("Todos os campos são necessários")
        else:
            novo_motorista  = Motoristas(nome=nome, rota=rota, celular=celular, regiao_id=regiao_id)
            db.session.add(novo_motorista)
            db.session.commit()
            flash("Motorista cadastrado com sucesso!")
            return redirect(url_for("cadastro_motoristas"))  # Evita resubmissão do formulário
        
    return render_template("cadastro_motoristas.html")

# Rota que realiza o cadasdtro dos alunos
@app.route("/cadastro_alunos", methods=["GET", "POST"])
#Função que verifica se o usuário está cadastrado.
def cadastro_alunos():
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login


    if request.method == "POST":
        nome = request.form.get("nome", "").upper().strip()
        celular = request.form.get("celular")
        regiao_id = request.form.get("regiao_id")  # Obtendo a ID da região selecionada
        motorista_id = request.form.get("motorista_id")  # Obtendo a ID do motorista selecionado
        cadastro_existente = Alunos.query.filter_by(nome=nome).first() #realiza a consulta no banco.
        #Verifica se o nome cadastrado já se encontra no banco de dados, se já constar retornará um aviso ao usuário
        if cadastro_existente:
            flash(f"Nome já consta cadastrado, verifique em exibir cadastro.")
            return render_template("cadastro_motoristas.html")
        
        #Verifica se todos os campos foram preenchidos. Se não forem não realiza o cadastro e retorna uma informação ao usuário.
        if not nome or not regiao_id or not motorista_id:
            flash("Todos os campos são necessários")
        else:
            novo_aluno = Alunos(nome=nome, celular=celular, regiao_id=regiao_id, motorista_id=motorista_id)
            db.session.add(novo_aluno)
            db.session.commit()
            flash("Aluno cadastrado com sucesso!")
            return redirect(url_for("cadastro_alunos"))  # Evita resubmissão do formulário

    #Carrega as regiões e os motoristas disponíveis para poder na criar a vinculação
    regioes = Regioes.query.all()  # Obtendo todas as regiões
    motoristas = Motoristas.query.all()  # Obtendo todos os motoristas
    return render_template("cadastro_alunos.html", motoristas=motoristas, regioes=regioes)

#Rota que retorna para o javascript a lista de motoristas por região
@app.route("/motoristas_por_regiao")
def obter_motoristas():
    regiao_id = request.args.get("regiao")
    if not regiao_id:
        return jsonify([])

    motoristas = Motoristas.query.filter_by(regiao_id=regiao_id).all()
    return jsonify([{"id": m.id, "nome": m.nome} for m in motoristas])


# Exibe a lista de motoristas cadastrados
@app.route("/motoristas", methods=["GET", "POST"])
def listar_motoristas(): 
    motoristas = Motoristas.query.all()
    if len(motoristas) == 0:
        flash("Não há motoristas cadastrados")
    return render_template("motoristas.html",motoristas=motoristas)

#Exibe a lista de alunos cadastrados
@app.route("/alunos", methods=["GET"])
def listar_alunos(): 
    alunos = Alunos.query.all()
    if len(alunos) == 0:
        flash("Não há alunos cadastrados")   
    return render_template("alunos.html",alunos=alunos)

#Exibe as rotas existentes vinculando os motoristas aos alunos.
@app.route("/rotas", methods=["GET", "POST"])
def relacao_rota():
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login          
    #Carrega as regiões e os motoristas disponíveis para poder na criar a vinculação
    alunos = Alunos.query.all()
    regioes = Regioes.query.all()  # Obtendo todas as regiões
    motoristas = Motoristas.query.all()  # Obtendo todos os motoristas
    if len(motoristas) == 0:
        flash("Não exite rotas disponíveis")
   
    return render_template("rotas.html",motoristas=motoristas, regioes=regioes, alunos=alunos)

#Edição do cadastro dos motoristas
@app.route('/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login
    regiao_id=Regioes.query.all()
    
    motorista = Motoristas.query.get(id)
    if not motorista:
        flash("Motorista não encontrado.")
        return redirect(url_for("motoristas"))

    if request.method == "POST":
        nome = request.form.get("nome", "").upper().strip()
        rota = request.form.get("rota", "").upper().strip()
        celular = request.form.get("celular")
        regiao_id = request.form.get("regiao_id")
        

        if not nome or not rota or not regiao_id or not celular:
            flash("Todos os campos são necessários.")
        else:
            motorista.nome = nome
            motorista.rota = rota
            motorista.celular = celular
            motorista.regiao_id = regiao_id

            db.session.commit()
            flash("Motorista atualizado com sucesso!")
            return redirect(url_for("cadastro_motoristas"))

    return render_template("edit_motorista.html", id=motorista.id, nome=motorista.nome, rota=motorista.rota, celular=motorista.celular, regiao_id=motorista.regiao_id, motorista=motorista)
    
#Edição do cadastro dos alunos
@app.route('/<int:id>/edit_aluno', methods=["GET", "POST"])
def edit_aluno(id):
    usuario_login = verifica_login()
    if usuario_login:
        return usuario_login
    motorista = Motoristas.query.all()
    regioes = Regioes.query.all()  # Obtendo todas as regiões
    aluno = Alunos.query.get(id)
    
    if not aluno:
        flash("Aluno não encontrado.")
        return redirect(url_for("alunos"))

    if request.method == "POST":
        nome = request.form.get("nome", "").upper().strip()
        celular = request.form.get("celular")
        regiao_id = request.form.get("regiao_id")
        motorista_id = request.form.get("motorista_id")  # Obtendo a ID do motorista selecionado

        

        if not nome or not regiao_id or not celular:
            flash("Todos os campos são necessários.")
        else:
            aluno.nome = nome
            aluno.celular = celular
            aluno.motorista_id = motorista_id
            aluno.regiao_id = regiao_id
            print(f'nome{nome},  celular {celular} regiao_id {regiao_id}')


            db.session.commit()
            flash("Aluno atualizado com sucesso!")
            return redirect(url_for("cadastro_alunos"))

    return render_template("edit_alunos.html", id=aluno.id, nome=aluno.nome, celular=aluno.celular,motorista_id=aluno.motorista_id, regiao_id=aluno.regiao_id, regioes=regioes, motorista=motorista, aluno=aluno)

#Rota que apaga o cadastro do motoristas    
@app.route('/<int:id>/delete', methods=["POST"])
def delete(id):
    motorista = Motoristas.query.get(id)
    if len(motorista.alunos) == 0:
        db.session.delete(motorista)
        db.session.commit()
        print(f"{motorista}")
        flash(f"{motorista.nome} deletado do cadastro")
        return render_template("edit_motorista.html", id=motorista.id, nome=motorista.nome, rota=motorista.rota, celular=motorista.celular, regiao_id=motorista.regiao_id, motorista=motorista)
    else:
      
        flash(f"{motorista.nome} tem alunos vinculados a ele. Para poder deletar o cadastro é preciso remover os alunos vinculados.")
        return render_template("edit_motorista.html", id=motorista.id, nome=motorista.nome, rota=motorista.rota, celular=motorista.celular, regiao_id=motorista.regiao_id, motorista=motorista)

#Rota que apaga o cadastro do aluno    
@app.route("/<int:id>/delete_aluno", methods=["POST"])
def delete_aluno(id):
    aluno = Alunos.query.get(id)
    motorista = Motoristas.query.all()
    regioes = Regioes.query.all() 
    db.session.delete(aluno)
    db.session.commit()
    flash(f"{aluno.nome} deletado do cadastro")
    return render_template("edit_alunos.html", id=aluno.id, nome=aluno.nome, celular=aluno.celular,motorista_id=aluno.motorista_id, regiao_id=aluno.regiao_id, regioes=regioes, motorista=motorista, aluno=aluno)
    


if __name__ == "__main__":
    app.run(debug=True)
