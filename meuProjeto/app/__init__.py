from app.config import Config
from flask import Flask, render_template


def Create_app():
  app = Flask(__name__, template_folder='views')
  app.config.from_object(Config)

  from .controllers.meu_cine import mf_bp

  app.register_blueprint(mf_bp)

  @app.errorhandler(404)
  def pagina_nao_encontrada(error):
    app.logger.warning(f'Página não encontrada (404): {error}')
    return render_template('404.html'), 404

  return app