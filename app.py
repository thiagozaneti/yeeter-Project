from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:thiago06102006@localhost/cadyeet"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'minhachave'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



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


@app.route("/login", methods = ['POST','GET'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        users = User.query.filter_by(email = email, password = password)
        if users:
            return render_template("home.html")
        else:
            message = "usuario nao encontrado, tente novamente"
            return render_template("index.html", message = message)
    return render_template('login.html')   



@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    db.create_all()
    app.run()
