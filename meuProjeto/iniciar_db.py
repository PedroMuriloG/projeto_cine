from app.database import DatabaseConnection
from werkzeug.security import generate_password_hash


def iniciar_banco():
  with DatabaseConnection() as db:
    db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

    db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                release_year INTEGER,
                poster_url TEXT,
                synopsis TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

    db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                rating REAL NOT NULL,
                is_fresh INTEGER NOT NULL DEFAULT 0,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE
            )
        """)

    # Usuário de teste inicial (anote essas credenciais para o README.md e resumo)
    teste_username = "teste_cine"
    teste_email = "teste@cineapp.com"
    teste_senha_hash = generate_password_hash("123456")

    db.cursor.execute(
        """
            INSERT OR IGNORE INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """,
        (teste_username, teste_email, teste_senha_hash),
    )

  print("Banco inicializado com sucesso!")


if __name__ == "__main__":
  iniciar_banco()