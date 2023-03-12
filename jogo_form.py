from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired

class JogoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    plataforma = SelectField('Plataforma', coerce=int, validators=[DataRequired()])
    categoria = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    imagem = FileField('Imagem')