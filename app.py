from flask import Flask, render_template, redirect, request, session, flash, url_for
from functools import wraps
import mysql.connector
import os
from werkzeug.utils import secure_filename
from jogo_form import JogoForm  # importar o formulário JogoForm

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Configurações do Banco de Dados
db = mysql.connector.connect(
  host="catalogo-games-db",
  user="admin",
  password="admin",
  database="db_games"
)

# Decorator para verificação de login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return decorated_function

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user is not None:
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect('/games')
        else:
            return render_template('login.html', message='Usuário ou senha incorretos!')
    else:
        return render_template('login.html')

# Rota para a página de jogos
@app.route('/games', methods=['GET'])
def games():
    if session.get('logged_in'):
        # Lógica de paginação
        page = request.args.get('page', 1, type=int)
        items_per_page = 10
        offset = (page - 1) * items_per_page
        
        # Lógica de filtro
        name_filter = request.args.get('name_filter', '')
        platform_filter = request.args.get('platform_filter', '')
        category_filter = request.args.get('category_filter', '')
        
        cursor = db.cursor()
        
        # Consulta com filtros
        query = f"SELECT * FROM games WHERE name LIKE '%{name_filter}%' AND platform LIKE '%{platform_filter}%' AND category LIKE '%{category_filter}%' ORDER BY id ASC LIMIT {items_per_page} OFFSET {offset}"
        cursor.execute(query)
        games = cursor.fetchall()
        
        # Consulta para contar o total de jogos (para a paginação)
        query = f"SELECT COUNT(*) FROM games WHERE name LIKE '%{name_filter}%' AND platform LIKE '%{platform_filter}%' AND category LIKE '%{category_filter}%'"
        cursor.execute(query)
        total_items = cursor.fetchone()[0]
        total_pages = int(total_items / items_per_page) + (total_items % items_per_page > 0)
        
        return render_template('games.html', games=games, page=page, total_pages=total_pages, name_filter=name_filter, platform_filter=platform_filter, category_filter=category_filter, username=session['username'])
    else:
        return redirect('/')

# Rota para adicionar novo jogo
@app.route('/jogos/novo', methods=['GET', 'POST'])
@login_required
def novo_jogo():
    form = JogoForm()
    plataformas = Plataforma.query.all()
    form.plataforma.choices = [(p.id, p.nome) for p in plataformas]

    categorias = Categoria.query.all()
    form.categoria.choices = [(c.id, c.nome) for c in categorias]

    if request.method == 'POST':
        nome = form.nome.data
        plataforma_id = form.plataforma.data
        categoria_id = form.categoria.data
        descricao = form.descricao.data
        imagem = form.imagem.data
        filename = secure_filename(imagem.filename)

        cursor = db.cursor()
        query = "INSERT INTO games (name, platform_id, category_id, description, image) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, plataforma_id, categoria_id, descricao, filename))
        db.commit()

        if imagem:
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Jogo adicionado com sucesso!', 'success')
        return redirect('/games')
    else:
        return render_template('novo_jogo.html', form=form)