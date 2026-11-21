from contextlib import contextmanager
import sqlite3


class Database:
  """Gerencia a conexão SQLite, o cursor e a criação das tabelas em um único lugar."""

  DB_FILE = "MEUS FILME PROJETO.db"

  @classmethod
  @contextmanager
  def get_db_cursor(cls):
    conn = sqlite3.connect(cls.DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
      yield cursor
      conn.commit()
    except Exception as e:
      conn.rollback()
      raise e
    finally:
      cursor.close()
      conn.close()

  @classmethod
  def init_db(cls):
    with cls.get_db_cursor() as cursor:
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

      cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    release_year INTEGER NOT NULL,
                    poster_url TEXT,
                    synopsis TEXT
                )
            """)

      cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    movie_id INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    is_fresh INTEGER NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE
                )
            """)