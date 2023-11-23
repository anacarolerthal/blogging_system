#Data Layer - conexao com o banco
import psycopg2 

DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

class BlogModel:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()
        
        #self.connection.commit()

    # def create_user(self, user):
    #     self.cursor.execute('INSERT INTO baseuser (username, email, passw, is_moderator) VALUES (%s, %s, %s, %s) RETURNING id', (user.username, user.email, user.password, ))
    #     self.connection.commit()
    #     fetched = self.cursor.fetchone()
    #     user.set_user_id(fetched[0])
    #     return user

    def create_post(self, post):
        self.cursor.execute('INSERT INTO post (title, text_content, image, author_id) VALUES (%s, %s, %s, %s) RETURNING id, creation_date', (post.title, post.content, post.image, post.author_id))
        self.connection.commit()
        fetched = self.cursor.fetchone()
        post.set_post_id(fetched[0])
        post.set_post_date(fetched[1])
        return post

    def create_reply(self, reply):
        self.cursor.execute('INSERT INTO reply (text_content, image, author_id, parent_post_id) VALUES (%s, %s, %s, %s) RETURNING id, creation_date', (comment.content, comment.image, comment.author_id, comment.parent_post_id))
        fetched = self.cursor.fetchone()
        reply.set_post_id(fetched[0])
        reply.set_post_date(fetched[1])
        return reply

    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM post')
        return self.cursor.fetchall()

    def get_n_posts(self, n, offset=0):
        self.cursor.execute('SELECT * FROM post LIMIT %s OFFSET %s', (n, offset))
        return self.cursor.fetchall()

    def get_replies_for_post(self, post):
        self.cursor.execute('SELECT * FROM reply WHERE parent_post_id = %s', (post.id))
        return self.cursor.fetchall()
    
    def check_user(self, username, password):
        self.cursor.execute('SELECT * FROM baseuser WHERE username = %s AND password = %s', (username, password))
        return bool(self.cursor.fetchone())
    
    def add_user(self, username, password, email):
        self.cursor.execute('INSERT INTO baseuser (username, password, email, is_moderator) VALUES (%s, %s, %s, %s)', (username, password, email, 0))
        self.connection.commit()
        
    def add_moderator(self, username, password, email):
        self.cursor.execute('INSERT INTO baseuser (username, password, email, is_moderator) VALUES (%s, %s, %s, %s)', (username, password, email, 1))
        self.connection.commit()

bg = BlogModel()
#bg.drop_table()
bg.create_table()
bg.check_user('admin', 'admin')