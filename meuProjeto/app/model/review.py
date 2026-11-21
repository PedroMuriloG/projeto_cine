from app.database import DatabaseConnection


class Review:

  def __init__(
      self,
      id,
      user_id,
      movie_id,
      rating,
      is_fresh,
      content,
      created_at=None,
      movie_title=None,
      poster_url=None,
  ):
    self.id = id
    self.user_id = user_id
    self.movie_id = movie_id
    self.rating = rating
    self.is_fresh = is_fresh
    self.content = content
    self.created_at = created_at
    self.movie_title = movie_title
    self.poster_url = poster_url

  @classmethod
  def criar(cls, user_id, movie_id, rating, is_fresh, content):
    sql = """
            INSERT INTO reviews (user_id, movie_id, rating, is_fresh, content)
            VALUES (?, ?, ?, ?, ?)
        """
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (user_id, movie_id, rating, is_fresh, content))
      return db.cursor.lastrowid

  @classmethod
  def listar_por_usuario(cls, user_id):
    sql = """
            SELECT r.*, m.title AS movie_title, m.poster_url
            FROM reviews r
            JOIN movies m ON r.movie_id = m.id
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        """
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (user_id,))
      rows = db.cursor.fetchall()
      return [
          cls(
              id=r['id'],
              user_id=r['user_id'],
              movie_id=r['movie_id'],
              rating=r['rating'],
              is_fresh=r['is_fresh'],
              content=r['content'],
              created_at=r['created_at'],
              movie_title=r['movie_title'],
              poster_url=r['poster_url'],
          )
          for r in rows
      ]

  @classmethod
  def excluir(cls, review_id, user_id):
    sql = 'DELETE FROM reviews WHERE id = ? AND user_id = ?'
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (review_id, user_id))
      return db.cursor.rowcount > 0