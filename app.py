from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carros.sqlite3'

db = SQLAlchemy(app)

class Carros(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column('marca', db.String(150))
    modelo = db.Column('modelo',db.String(60))
    ano = db.Column('ano', db.Integer)

    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano


@app.route('/')
def index():
    carros = Carros.query.all()
    return render_template("index.html", carros=carros)

@app.route('/add', methods=['GET','POST'])
def add_carro():
    if request.method == 'POST':
        carro = Carros(request.form["marca"], request.form['modelo'], request.form['ano'])
        db.session.add(carro)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_carro(id):
    carro = Carros.query.get(id)    
    db.session.delete(carro)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET','POST'])
def update_carro(id):
    carro = Carros.query.get(id)
    if request.method == 'POST':
        carro.marca = request.form["marca"]
        carro.modelo = request.form['modelo']
        carro.ano =  request.form['ano']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', carro=carro)

if __name__ == "__main__":
    app.run(debug=True)