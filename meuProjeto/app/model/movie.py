from app.database import DatabaseConnection


class Movie:

  def __init__(self, id, user_id, title, release_year, poster_url, synopsis):
    self.id = id
    self.user_id = user_id
    self.title = title
    self.release_year = release_year
    self.poster_url = poster_url
    self.synopsis = synopsis

  @classmethod
  def criar(cls, user_id, title, release_year, poster_url, synopsis):
    sql = """
            INSERT INTO movies (user_id, title, release_year, poster_url, synopsis)
            VALUES (?, ?, ?, ?, ?)
        """
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (user_id, title, release_year, poster_url, synopsis))
      return db.cursor.lastrowid

  @classmethod
  def listar_por_usuario(cls, user_id):
    sql = """
            SELECT id, user_id, title, release_year, poster_url, synopsis
            FROM movies
            WHERE user_id = ?
            ORDER BY id DESC
        """
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (user_id,))
      rows = db.cursor.fetchall()
      return [
          cls(
              r['id'],
              r['user_id'],
              r['title'],
              r['release_year'],
              r['poster_url'],
              r['synopsis'],
          )
          for r in rows
      ]

  @classmethod
  def buscar_por_id_e_usuario(cls, movie_id, user_id):
    sql = """
            SELECT id, user_id, title, release_year, poster_url, synopsis
            FROM movies
            WHERE id = ? AND user_id = ?
        """
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (movie_id, user_id))
      row = db.cursor.fetchone()
      if row:
        return cls(
            row['id'],
            row['user_id'],
            row['title'],
            row['release_year'],
            row['poster_url'],
            row['synopsis'],
        )
    return None

  @classmethod
  def excluir(cls, movie_id, user_id):
    sql = 'DELETE FROM movies WHERE id = ? AND user_id = ?'
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (movie_id, user_id))
      return db.cursor.rowcount > 0