from app.database import DatabaseConnection
from werkzeug.security import check_password_hash, generate_password_hash


class User:

  def __init__(self, id, username, email, password_hash):
    self.id = id
    self.username = username
    self.email = email
    self.password_hash = password_hash

  @classmethod
  def salvar(cls, username, email, password):
    password_hash = generate_password_hash(password)
    sql = """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """
    try:
      with DatabaseConnection() as db:
        db.cursor.execute(sql, (username, email, password_hash))
        user_id = db.cursor.lastrowid
        return cls(user_id, username, email, password_hash)
    except Exception:
      return None

  @classmethod
  def buscar_por_email(cls, email):
    sql = 'SELECT id, username, email, password_hash FROM users WHERE email = ?'
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (email,))
      row = db.cursor.fetchone()
      if row:
        return cls(row['id'], row['username'], row['email'], row['password_hash'])
    return None

  @classmethod
  def buscar_por_id(cls, user_id):
    sql = 'SELECT id, username, email, password_hash FROM users WHERE id = ?'
    with DatabaseConnection() as db:
      db.cursor.execute(sql, (user_id,))
      row = db.cursor.fetchone()
      if row:
        return cls(row['id'], row['username'], row['email'], row['password_hash'])
    return None

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)