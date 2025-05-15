from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify


app = Flask(__name__)
app.secret_key = 'temosUmaChaveAqui102' #chave secreta faz com o cookie salve as informações que só podem ser acessadas por quem tem a chave.

motoristas_por_regiao = {
    "Norte": ["João Silva", "Ana Pereira"],
    "Sul": ["Carlos Oliveira", "Fernanda Lima"],
    "Leste": ["Roberto Souza", "Beatriz Ramos"],
    "Oeste": ["Mariana Costa", "Ricardo Alves"]
}


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
        
        usuario = request.form["usuario"]
        senha = request.form["senha"]
    
        #Controle de acesso.
        if usuario == "Pedro" and senha == "123":
            session['usuario_logado'] = True 
            session['nome'] = usuario
            return redirect(url_for("home"))
        else:
            erro = "Usuário ou senha inválidos!"
            return render_template('login.html', erro=erro) 
    return render_template('login.html') 

@app.route("/home")
def home():
    if not session.get("usuario_logado", False):

        return render_template('login.html')
    nome = f"Bem vindo, {session['nome']}"
    return render_template("home.html", nome=nome)      

@app.route("/logout")
def logout():
    session.pop('usuario_logado', None)
    session.pop('nome', None)
    return redirect(url_for("index"))

@app.route("/cadastro")
def cadastro():
    if not session.get("usuario_logado", False):

        return render_template('login.html')
    return render_template("/cadastro.html")


@app.route("/rotas")
def rotas():
    return render_template("rotas.html", motoristas_por_regiao=motoristas_por_regiao)
@app.route("/motoristas", methods=["GET"])

def get_motoristas():
    regiao = request.args.get("regiao") 
    motoristas = motoristas_por_regiao.get(regiao, [])  
    return jsonify(motoristas)  


if __name__ == "__main__":
    app.run(debug=True)