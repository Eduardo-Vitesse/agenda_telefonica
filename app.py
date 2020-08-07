from flask import Flask, render_template, request, redirect, url_for, flash
from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy

# Configurações global
app = Flask(__name__)
secret_key = 'um-nome-bem-seguro'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações de variáveis global
ui = FlaskUI(app)
db = SQLAlchemy(app)


# Classe do banco de dados
class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def __init__(self, number, name, status, data, hora, description):
        self.number = number
        self.name = name
        self.status = status
        self.data = data
        self.hora = hora
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.id


# Rotas
@app.route("/", methods=['GET'])
def index():
    all_data = Number.query.all()

    return render_template("index.html", contatos=all_data)


@app.route("/create", methods=['POST'])
def create():
    if request.method == 'POST':
        number = request.form['number']
        name = request.form['name']
        status = request.form['status']
        data = request.form['data']
        hora = request.form['hora']
        description = request.form['description']

        data = Number(number, name, status, data, hora, description)
        db.session.add(data)
        db.session.commit()

        # flash("Contato criado com sucesso!")
        return redirect(url_for("index"))


@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = Number.query.get(request.form.get('id'))

        data.number = request.form['number']
        data.name = request.form['name']
        data.status = request.form['status']
        data.data = request.form['data']
        data.hora = request.form['hora']
        data.description = request.form['description']

        db.session.commit()
        # flash("Contato atualizado com sucesso!")
        return redirect(url_for("index"))


@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    data = Number.query.get(id)
    db.session.delete(data)
    db.session.commit()
    # flash("Contato deletado...")
    return redirect(url_for("index"))


# call the 'run' method
ui.run()