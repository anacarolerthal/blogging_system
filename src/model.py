#Data Layer - conexao com o banco
import psycopg2 

DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

class BlogModel:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        ''')
        self.connection.commit()

    def create_post(self, title, content):
        self.cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        self.connection.commit()

    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM posts')
        return self.cursor.fetchall()