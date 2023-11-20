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
                id SERIAL PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                content TEXT,
                parent_post_id INTEGER REFERENCES posts(id)
            )
        ''')

        self.connection.commit()

    def create_post(self, post):
        self.cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id', (post.title, post.content))
        self.connection.commit()
        post_id = self.cursor.fetchone()[0]
        return post_id

    def create_comment(self, comment):
        self.cursor.execute('INSERT INTO comments (content, parent_post_id) VALUES (%s, %s) RETURNING id', (comment.title, comment.parent_post_id))
        self.connection.commit()
        comment_id = self.cursor.fetchone()[0]
        return comment_id

    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM posts')
        return self.cursor.fetchall()

    def get_comments_for_post(self, post):
        self.cursor.execute('SELECT * FROM comments WHERE parent_post_id = %s', (post.id,))
        return self.cursor.fetchall()