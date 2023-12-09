#Data Layer - conexao com o banco
import psycopg2

#def
#DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"
#user postgres, password admin, database blogdb
DATABASE_URL = "postgres://postgres:admin@localhost:5432/blogdb"
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
        
    # def __del__(self):
    #     self.cursor.close()
    #     self.connection.close()

    def create_post(self, post):
        self.cursor.execute('INSERT INTO Post (author_id, title, text_content, image) VALUES (%s, %s, %s, %s) RETURNING id', 
                            (post.author_id, post.title, post.content, post.image))
        id = self.cursor.fetchone()[0]
        self.connection.commit()
        return id

    def create_reply(self, reply):
        self.cursor.execute('INSERT INTO Reply (author_id, text_content, image, parent_post_id) VALUES (%s, %s, %s, %s) RETURNING id', 
                            (reply.author_id, reply.content, reply.image, reply.parent_post_id))
        id = self.cursor.fetchone()[0]
        self.connection.commit()
        return id
    
    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM Post')
        return self.cursor.fetchall()
    
    def get_n_posts(self, n, offset=0):
        self.cursor.execute('SELECT * FROM Post LIMIT %s OFFSET %s', (n, offset))
        return self.cursor.fetchall()

    def get_comments_for_post(self, postId):
        self.cursor.execute('SELECT * FROM Reply WHERE parent_post_id = %s', (postId,))
        return self.cursor.fetchall()

    def check_user(self, username, password):
        self.cursor.execute('SELECT * FROM baseuser WHERE username = %s AND passw = %s', (username, password))
        return bool(self.cursor.fetchone())

    def get_user_id_by_username(self, username):
        self.cursor.execute('SELECT id FROM baseuser WHERE username = %s', (username, ))
        return self.cursor.fetchone()

    def add_user(self, username, password, email):
        self.cursor.execute('INSERT INTO baseuser (username, passw, email, is_moderator) VALUES (%s, %s, %s, %s) RETURNING id', (username, password, email, False))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return user_id

    def follow(self, follower, followee):
        self.cursor.execute('INSERT INTO userfollows (follower_id, followee_id) VALUES (%s,%s)', (follower, followee))
        self.connection.commit()
    
    def unfollow(self, follower, followee):
        self.cursor.execute('DELETE FROM userfollows WHERE follower_id = %s AND followee_id = %s', (follower, followee))
        self.connection.commit()
    
    def get_following_user(self, user_id):
        self.cursor.execute('SELECT followee_id FROM userfollows WHERE follower_id = %s', (user_id,))
        out = self.cursor.fetchall()
        id_lists = []
        for id in out:
            id_lists.append(id[0])
        return id_lists
    
    def get_followers_user(self, user_id):
        self.cursor.execute('SELECT follower_id FROM userfollows WHERE followee_id = %s', (user_id,))
        out = self.cursor.fetchall()
        id_lists = []
        for id in out:
            id_lists.append(id[0])
        return id_lists

    def check_if_user_in_db(self, user_id):
        self.cursor.execute('SELECT * FROM baseuser WHERE id = %s', (user_id,))
        return bool(self.cursor.fetchone())