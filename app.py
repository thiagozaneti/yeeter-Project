
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    
    

@app.route("/", methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == "POST":
        id = request.form['id']
        username = request.form['username']
        email = request.form['email'] 
        senha = request.form['senha']  
        
        if len(senha) <=4:
            message = f"senha fraca"
        if len(email) <=5:
            message = f'email fraco'
        if len(username) <=4:
            message = f'nome de usuario fraco'
        else:
            user = User(email=email, senha=senha, username = username, id = id)  
            db.session.add(user)
            db.session.commit()
            message="cadastro realizado com sucesso!"
            return redirect(url_for('home.html', username = username))
    
    return render_template("index.html", message=message)

@app.route("/login")
def cad():
    msg = "login efetuado com sucesso"
    return render_template("index.html", msg=msg)

db.init_app(app)

if __name__ == "__main__":
    db.init_app(app)
    db.create_all()
    app.run()
