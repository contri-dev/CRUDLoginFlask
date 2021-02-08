from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *
import json
import requests


#configuração app
app = Flask(__name__)
app.secret_key = 'replace later'

#configuração banco de dados
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost/Ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#configuração flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(cpf_cliente):

    return User.query.get(cpf_cliente)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrarForm()

    if reg_form.validate_on_submit():
        cpf = reg_form.cpf.data
        nome = reg_form.nome.data
        cep = reg_form.cep.data
        telefone = reg_form.telefone.data
        username = reg_form.username.data
        senha = reg_form.senha.data
        email = reg_form.email.data

        #Hash senha
        hashed_senha = pbkdf2_sha256.hash(senha)

        hashed_nome = cisco_type7.hash(nome)

        #Check username and CPF exists
        u_object = User.query.filter_by(login=username).all()
        if u_object:
            return "Alguem já está utilizando este usuário!"

        cpf_object = User.query.filter_by(cpf_cliente=cpf).all()
        if cpf_object:
            return "Esse cpf já está cadastrado."

        # Adicionando cliente ao banco de dados
        cliente = User(cpf_cliente=cpf, nome=hashed_nome, cep=cep, telefone=telefone, login=username, senha=hashed_senha, email=email)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(login=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('checkout'))

    return render_template("login.html", form=login_form)

@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if not current_user.is_authenticated:
        return
    nome = current_user.nome
    nome = cisco_type7.decode(nome)
    cep = current_user.cep
    cpf = current_user.cpf_cliente
    email = current_user.email
    telefone = current_user.telefone
    login= current_user.login
    try:
        URL = 'https://viacep.com.br/ws/'+cep+'/json/'
        endereco = requests.request('GET', URL)
        endereco = endereco.json()
        inexistente = False
    except:
        erro = 'CEP Inexistente'
        inexistente = True
        return render_template('checkout.html', erro = erro, inexistente = inexistente, nome = nome, cpf = cpf, email=email)
    try:
        rua = endereco["logradouro"]
    except:
        erro = 'CEP Inexistente'
        inexistente = True
        return render_template('checkout.html', erro = erro, inexistente = inexistente, nome = nome)
    bairro = endereco["bairro"]
    cidade = endereco["localidade"]
    estado = endereco["uf"]
    ddd = endereco["ddd"]
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        db.session.query(User).filter_by(login=login).delete()
        db.session.commit()
        return redirect(url_for('needlogin'))

    return render_template("checkout.html", nome = nome, rua = rua, bairro = bairro, cidade = cidade, estado = estado, ddd = ddd, cep = cep, cpf = cpf, email = email, telefone = telefone, form=delete_form  )

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/update", methods=['GET', 'POST'])
def update():
    update_form = UpdateForm()
    if not current_user.is_authenticated:
        return redirect(url_for('needlogin'))
    if update_form.validate_on_submit():
        n_cpf = update_form.cpf.data or None
        n_nome = update_form.nome.data or None
        n_cep = update_form.cep.data or None
        n_telefone = update_form.telefone.data or None
        n_username = update_form.username.data or None
        n_email = update_form.email.data or None

        login = current_user.login


        if n_nome != None:
            n_nome = cisco_type7.hash(n_nome)
            db.session.query(User).filter_by(login=login).update({User.nome:n_nome})
            db.session.commit()

        if n_cpf != None:
            db.session.query(User).filter_by(login=login).update({User.cpf_cliente:n_cpf})
            db.session.commit()

        if n_cep != None:
            db.session.query(User).filter_by(login=login).update({User.cep:n_cep})
            db.session.commit()

        if n_telefone != None:
            db.session.query(User).filter_by(login=login).update({User.telefone:n_telefone})
            db.session.commit()

        if n_email != None:
            db.session.query(User).filter_by(login=login).update({User.email:n_email})
            db.session.commit()

        if n_username != None:
            db.session.query(User).filter_by(login=login).update({User.login:n_username})
            db.session.commit()

        return redirect(url_for('checkout'))


    return render_template('update.html', form=update_form)

@app.route("/needlogin", methods=['GET'])
def needlogin():
    return render_template('needlogin.html')


if __name__ == "__main__":
    app.run(debug=True)
