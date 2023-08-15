from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'minhachave'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False) 
    senha = db.Column(db.String(20), nullable=False)  

@app.route("/", methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == "POST":
        id = request.form['id']
        username = request.form['username']
        email = request.form['email']
        senha = request.form['senha']
        
        if len(senha) <= 4:
            message = "Senha fraca"
        elif len(email) <= 5:
            message = "E-mail fraco"
        elif len(username) <= 4:
            message = "Nome de usuário fraco"
        else:
            user = User(id=id, username=username, email=email, senha=senha)  
            db.session.add(user)
            db.session.commit()
            message = "Cadastro realizado com sucesso!"
            return render_template('home.html', username=username)
    
    return render_template("index.html", message=message)

@app.route("/login")
def cad():
    msg = "Login efetuado com sucesso"
    return render_template("index.html", msg=msg)

if __name__ == "__main__":
    db.create_all()
    app.run()
