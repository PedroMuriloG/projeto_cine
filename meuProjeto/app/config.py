import os


class Config:
  SECRET_KEY = (
      os.environ.get("SECRET_KEY") or "sua_chave_secreta_super_segura"
  )

  BASE_DIR = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..")
  )  # ajuste se o config.py já estiver na raiz
  DATABASE_PATH = os.path.join(BASE_DIR, "MEUS FILMES PROJETO.db")