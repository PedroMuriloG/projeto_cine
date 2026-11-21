from functools import wraps
from app.model.user import User  # ou app.models.user, conforme o nome da sua pasta
from flask import flash, g, redirect, session, url_for


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    user_id = session.get('user_id')
    if not user_id:
      flash('Faça login para acessar esta página.', 'error')
      return redirect(url_for('filme.login'))

    usuario = User.buscar_por_id(user_id)
    if not usuario:
      session.clear()
      flash('Sessão inválida. Faça login novamente.', 'error')
      return redirect(url_for('filme.login'))

    g.usuario = usuario
    return f(*args, **kwargs)

  return decorated_function