from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar', validators=[DataRequired(), EqualTo('senha')])
    tipo = SelectField('Tipo', choices=[('profissional','Profissional'),('coordenador','Coordenador'),('adm','ADM')])
    submit = SubmitField('Registrar')

class PacienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[Optional()])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()], format='%Y-%m-%d')
    diagnostico = StringField('Diagnóstico', validators=[Optional()])
    responsavel = StringField('Responsável', validators=[Optional()])
    submit = SubmitField('Salvar')

class EvolucaoForm(FlaskForm):
    anotacao = TextAreaField('Anotação', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Salvar')
