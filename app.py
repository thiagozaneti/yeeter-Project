from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:thiago06102006@localhost/cadyeet"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'minhachave'
db = SQLAlchemy(app)

class User(db.Model, UserMixin): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Postagem(db.Model):
    __tablename__ = "postagem"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), unique=True, nullable=False)
    mensagem = db.Column(db.String(500), unique=True, nullable=False)
    
login_manager = LoginManager(app)

@login_manager.user_loader    #A função load_user é usada pelo Flask-Login para carregar um objeto de usuário com base no user_id armazenado na sessão do usuário. Isso permite que o Flask-Login mantenha o controle da sessão do usuário.
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['senha']
        
        if len(password) <= 4:
            message = "Senha fraca"
        elif len(email) <= 5:
            message = "E-mail fraco"
        elif len(username) <= 4:
            message = "Nome de usuário fraco"
        elif len(username) > 20:
            message = "Usuário excedente, mínimo 20 caracteres"
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            message = "Cadastro realizado com sucesso!"
            return render_template('login.html', username=username)
        
        repeat_user = User.query.filter_by(username=username, email=email, password=password).first()
        if repeat_user:
            message = "Usuário já existente, faça login"
            return render_template("login.html", message=message)
        
    return render_template("index.html", message=message)

@app.route("/login", methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user) #quando é autenticado, o flask cria uma sessao de usuario adequeda, mantendo o usuario autenticado
            return render_template("home.html")
        else:
            message = "Usuário não encontrado, tente novamente"
            return render_template("index.html", message=message)
    return render_template('login.html')

@app.route('/perfil') ##rota de perfil com a protecao do required
@login_required ##login required é priovado, nao erve para ambiente globais
def perfil():
    return render_template("perfil.html", username=current_user.username, password = current_user.password, email = current_user.email)

@app.route("/home")
def home():
    postagens = Postagem.query.all()
    return render_template("home.html", postagens = postagens)
#teste
@app.route('/postagem', methods=['POST','GET'])
def postagem():
    if request.method == 'POST':
        titulo = request.form['titulo']
        mensagem = request.form['mensagem']
        new_mensagem = Postagem(titulo = titulo, mensagem = mensagem)
        db.session.add(new_mensagem) ##adicona a variável aq 
        db.session.commit()
    return render_template('postagem.html')

@app.route('/sair')
def sair():
    return render_template('index.html')


if __name__ == "__main__":
    db.create_all()
    app.run()
