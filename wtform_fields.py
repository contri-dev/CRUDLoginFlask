from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User
from passlib.hash import pbkdf2_sha256, cisco_type7

def invalid_credentials(form, field):
    """ Login e senha checker """

    username_entered =  form.username.data
    password_entered = field.data

    #Checando credenciais
    user_object = User.query.filter_by(login=username_entered).first()
    if user_object is None:
        raise ValidationError("Login ou senha está incorreto")
    elif not pbkdf2_sha256.verify(password_entered, user_object.senha):
        raise ValidationError("Login ou senha está incorreto")

class RegistrarForm(FlaskForm):
    """ Formulario de registro """

    nome = StringField('nome_label', validators=[InputRequired(message="Nome requerido")])
    cpf = IntegerField('cpf_label', validators=[InputRequired(message="CPF requerido")])
    cep = StringField('cep_label', validators=[InputRequired(message="CEP requerido")])
    telefone = IntegerField('cep_label', validators=[InputRequired(message="Telefone requerido")])
    email = StringField('email_label', validators=[InputRequired(message="Email requerido"), Length(min=4, max=25, message="O email precisa conter entre 4 e 25 caracteres")])
    username = StringField('username_label', validators=[InputRequired(message="Usuario requerido"), Length(min=4, max=25, message="O usuario precisa conter entre 4 e 25 caracteres")])
    senha = PasswordField('senha_label', validators=[InputRequired(message="Senha requerida"), Length(min=4, max=25, message="A senha precisa conter entre 4 e 25 caracteres")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Senha requerida"), EqualTo('senha', message="As senhas devem ser iguais")])
    submit_button = SubmitField('Criar')

class LoginForm(FlaskForm):
    """ Formulario de login """

    username= StringField('username_label', validators=[InputRequired(message="Usuario requerido")])
    senha= PasswordField('senha_label', validators=[InputRequired(message="Senha requerida"), invalid_credentials])
    submit_button = SubmitField('Entrar')

class UpdateForm(FlaskForm):
    """ Formulario de Update"""

    nome = StringField('nome_label')
    cpf = StringField('cpf_label')
    cep = StringField('cep_label')
    telefone = StringField('cep_label')
    email = StringField('email_label')
    username = StringField('username_label')
    submit_button = SubmitField('Atualizar')

class DeleteForm(FlaskForm):
    submit_button = SubmitField('Deletar conta')
