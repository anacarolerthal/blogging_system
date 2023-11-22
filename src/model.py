#Data Layer - conexao com o banco
import psycopg2

DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

class BlogModel:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()

    def drop_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS *')
        self.connection.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title TEXT,
                content TEXT,
                author_id INTEGER REFERENCES users(id),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                content TEXT,
                parent_post_id INTEGER REFERENCES posts(id),
                author_id INTEGER REFERENCES users(id),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT,
                password TEXT,
                email TEXT
            )
        ''')

        self.connection.commit()


    def create_user(self, name, email):
        self.cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id', (name, email))
        self.connection.commit()
        fetched = self.cursor.fetchone()
        #user.set_user_id(fetched[0])
        #return user

    def create_post(self, post):
        self.cursor.execute('INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s) RETURNING id, date', (post.title, post.content, post.author_id))
        self.connection.commit()
        fetched = self.cursor.fetchone()
        post.set_post_id(fetched[0])
        post.set_post_date(fetched[1])
        return post

    def create_comment(self, comment):
        self.cursor.execute('INSERT INTO comments (content, parent_post_id, author_id) VALUES (%s, %s, %s) RETURNING id, date', (comment.content, comment.parent_post.id, comment.author_id))
        fetched = self.cursor.fetchone()
        comment.set_post_id(fetched[0])
        comment.set_post_date(fetched[1])
        return comment

    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM posts')
        return self.cursor.fetchall()

    def get_n_posts(self, n, offset=0):
        self.cursor.execute('SELECT * FROM posts LIMIT %s OFFSET %s', (n, offset))
        return self.cursor.fetchall()

    def get_comments_for_post(self, post):
        self.cursor.execute('SELECT * FROM comments WHERE parent_post_id = %s', (post.id,))
        return self.cursor.fetchall()
    
    def check_user(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        return bool(self.cursor.fetchone())
    
# bg = BlogModel()
# bg.create_table()
# bg.check_user('admin', 'admin')