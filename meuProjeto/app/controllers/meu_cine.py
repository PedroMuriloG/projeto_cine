from app.model.movie import Movie
from app.model.review import Review
from app.model.user import User
from app.middleware.auth_middleware import login_required
from flask import Blueprint, current_app, flash, g, make_response, redirect, render_template, request, session, url_for

mf_bp = Blueprint('filme', __name__)


# --- Rota para Adicionar um Novo Filme no Catálogo ---
@mf_bp.route('/filmes/novo', methods=['GET', 'POST'])
@login_required
def adicionar_filme():
  if request.method == 'POST':
    title = request.form.get('title', '').strip()
    release_year = request.form.get('release_year', '').strip()
    poster_url = request.form.get('poster_url', '').strip()
    synopsis = request.form.get('synopsis', '').strip()

    if not title or len(title) > 150:
      flash('O título do filme é obrigatório (máx. 150 caracteres).', 'error')
      return render_template('adicionar_filme.html')

    if release_year and not release_year.isdigit():
      flash('O ano de lançamento deve ser um número válido.', 'error')
      return render_template('adicionar_filme.html')

    ano_int = int(release_year) if release_year else None
    Movie.criar(g.usuario.id, title, ano_int, poster_url, synopsis)
    current_app.logger.info(
        f'Filme "{title}" cadastrado por user_id={g.usuario.id}'
    )
    flash('Filme adicionado ao catálogo com sucesso!', 'success')
    return redirect(url_for('filme.listar_filmes'))

  return render_template('adicionar_filme.html')


# --- Rota para Excluir um Filme ---
@mf_bp.route('/filmes/<int:movie_id>/excluir', methods=['POST'])
@login_required
def excluir_filme(movie_id):
  if Movie.excluir(movie_id, g.usuario.id):
    current_app.logger.info(
        f'Filme id={movie_id} excluído por user_id={g.usuario.id}'
    )
    flash('Filme excluído com sucesso!', 'success')
  else:
    flash('Filme não encontrado ou sem permissão para excluir.', 'error')
  return redirect(url_for('filme.listar_filmes'))


# --- Rota para Deixar uma Nota e Impressão de um Filme ---
@mf_bp.route('/filmes/<int:movie_id>/avaliar', methods=['GET', 'POST'])
@login_required
def avaliar_filme(movie_id):
  movie = Movie.buscar_por_id_e_usuario(movie_id, g.usuario.id)
  if not movie:
    flash('Filme não encontrado.', 'error')
    return redirect(url_for('filme.listar_filmes'))

  if request.method == 'POST':
    try:
      rating = float(request.form.get('rating', 5.0))
    except ValueError:
      flash('Nota inválida.', 'error')
      return render_template('avaliar_filme.html', movie=movie)

    if rating < 0 or rating > 5:
      flash('A nota deve estar entre 0 e 5.', 'error')
      return render_template('avaliar_filme.html', movie=movie)

    is_fresh = 1 if request.form.get('is_fresh') == 'on' else 0
    content = request.form.get('content', '').strip()

    Review.criar(
        user_id=g.usuario.id,
        movie_id=movie_id,
        rating=rating,
        is_fresh=is_fresh,
        content=content,
    )
    current_app.logger.info(
        f'Avaliação criada para movie_id={movie_id} por user_id={g.usuario.id}'
    )
    flash(f'Adicionaste "{movie.title}" à tua estante!', 'success')
    return redirect(url_for('filme.estante'))

  return render_template('avaliar_filme.html', movie=movie)


# --- Rota da Estante Pessoal (Estilo Letterboxd) ---
@mf_bp.route('/estante')
@login_required
def estante():
  reviews = Review.listar_por_usuario(g.usuario.id)
  return render_template('estante.html', reviews=reviews)


# --- Rota para Excluir uma Avaliação da Estante ---
@mf_bp.route('/estante/<int:review_id>/excluir', methods=['POST'])
@login_required
def excluir_avaliacao(review_id):
  if Review.excluir(review_id, g.usuario.id):
    current_app.logger.info(
        f'Avaliação id={review_id} excluída por user_id={g.usuario.id}'
    )
    flash('Avaliação removida da tua estante!', 'success')
  else:
    flash('Avaliação não encontrada ou sem permissão para excluir.', 'error')
  return redirect(url_for('filme.estante'))


@mf_bp.route('/')
def index():
  movies = (
      Movie.listar_por_usuario(session['user_id'])
      if 'user_id' in session
      else []
  )
  return render_template('home.html', movies=movies)


@mf_bp.route('/login', methods=['GET', 'POST'])
def login():
  ultimo_email = request.cookies.get('ultimo_email', '')

  if request.method == 'POST':
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
      flash('Preencha e-mail e senha.', 'error')
      return render_template('login.html', ultimo_email=email)

    user = User.buscar_por_email(email)
    if user and user.check_password(password):
      session.clear()
      session['user_id'] = user.id
      session['username'] = user.username
      current_app.logger.info(f'Login realizado: {user.email}')
      flash(f'Bem-vindo(a) de volta, {user.username}!', 'success')

      resp = make_response(redirect(url_for('filme.home')))
      resp.set_cookie('ultimo_email', email, max_age=60 * 60 * 24 * 7)
      return resp
    else:
      current_app.logger.warning(f'Falha de autenticação para: {email}')
      flash('Tente novamente! Informações inválidas.', 'error')

  return render_template('login.html', ultimo_email=ultimo_email)


@mf_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if len(username) < 3 or not email or len(password) < 4:
      flash(
          'Preencha usuário (mín. 3 caracteres), e-mail e senha (mín. 4'
          ' caracteres).',
          'error',
      )
      return render_template('cadastro.html')

    new_user = User.salvar(username, email, password)
    if new_user:
      current_app.logger.info(f'Novo usuário cadastrado: {email}')
      flash(
          'Cadastro realizado com sucesso! Faça login para continuar.', 'success'
      )
      return redirect(url_for('filme.login'))

    flash('Erro ao cadastrar. E-mail ou Nome de Usuário já em uso.', 'error')

  return render_template('cadastro.html')


@mf_bp.route('/logout')
def logout():
  current_app.logger.info(f"Logout do usuário ID: {session.get('user_id')}")
  session.clear()
  flash('Você saiu da sua sessão.', 'success')
  return redirect(url_for('filme.login'))


@mf_bp.route('/home')
def home():
  movies = (
      Movie.listar_por_usuario(session['user_id'])
      if 'user_id' in session
      else []
  )
  return render_template('home.html', movies=movies)


@mf_bp.route('/filmes')
@login_required
def listar_filmes():
  movies = Movie.listar_por_usuario(g.usuario.id)
  return render_template('lista_filmes.html', movies=movies)