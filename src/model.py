#Data Layer - conexao com o banco
import psycopg2

#def
DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

#singleton to ensure just one connection
class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
    
@Singleton
class DBConnection():
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)

class BlogModel:
    def __init__(self):
        self.connection = DBConnection.Instance().connection
        self.cursor = self.connection.cursor()

    def create_post(self, post):
        self.cursor.execute('INSERT INTO Post (author_id, title, text_content, image) VALUES (%s, %s, %s, %s) RETURNING id', 
                            (post.author_id, post.title, post.content, post.image))
        id = self.cursor.fetchone()[0]
        self.connection.commit()
        return id

    def create_reply(self, reply):
        self.cursor.execute('INSERT INTO Reply (author_id, text_content, image, parent_post_id) VALUES (%s, %s, %s, %s) RETURNING id', 
                            (reply.author_id, reply.content, reply.image, reply.parent_post_id))
        id = self.cursos.fetchone()[0]
        self.connection.commit()
        return None
    
    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM Post')
        return self.cursor.fetchall()
    
    def get_n_posts(self, n, offset=0):
        self.cursor.execute('SELECT * FROM Post LIMIT %s OFFSET %s', (n, offset))
        return self.cursor.fetchall()

    def get_comments_for_post(self, post):
        self.cursor.execute('SELECT * FROM comments WHERE parent_post_id = %s', (post.id,))
        return self.cursor.fetchall()

    def check_user(self, username, password):
        self.cursor.execute('SELECT * FROM baseuser WHERE username = %s AND passw = %s', (username, password))
        return bool(self.cursor.fetchone())
    
    def add_user(self, username, password, email):
        self.cursor.execute('INSERT INTO baseuser (username, passw, email, is_moderator) VALUES (%s, %s, %s, %s)', (username, password, email, False))
        self.connection.commit()
    