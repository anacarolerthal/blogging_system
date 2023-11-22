#Data Layer - conexao com o banco
import psycopg2

DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

class BlogModel:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()

    def drop_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS users CASCADE')
        self.connection.commit()

    def create_table(self):      
        #User table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER serial PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                admin BOOLEAN DEFAULT FALSE
            )
        ''')

        #Unique identifier for posts and comments
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS postIdentifier (
                id SERIAL PRIMARY KEY,
                author_id INTEGER REFERENCES users(id),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ''')

        #Post table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER REFERENCES postIdentifier(id),
                title TEXT NOT NULL,
                content TEXT,
                image TEXT
            )
        ''')

        #Comment table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER REFERENCES postIdentifier(id),
                content TEXT,
                image TEXT,
                parent_post_id INTEGER REFERENCES posts(id)
            )
        ''')

        #Tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        #Relation table for likes and users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS postLikes (
                id INTEGER REFERENCES postIdentifier(id),
                user_id INTEGER REFERENCES users(id),
                UNIQUE(id, user_id)
            )
        ''')

        #Relation table for followers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS userFollows (
                id INTEGER REFERENCES users(id)
                follower_id INTEGER REFERENCES users(id),
                UNIQUE(id, follower_id)
            )
        ''')

        #Relation for banned users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bannedUsers (
                id INTEGER REFERENCES users(id),
                banned_id INTEGER REFERENCES users(id),
                UNIQUE(id, banned_id)
            )
        ''')

        #Relation for tags and posts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS postTags (
                id INTEGER REFERENCES postIdentifier(id),
                tag_id INTEGER REFERENCES tags(id),
                UNIQUE(id, tag_id)
            )
        ''')

        # create a new user
        self.cursor.execute('INSERT INTO users (name, email, password, admin) VALUES (%s, %s, %s, %s)', ('admin', 'admin', 'admin', True))
        
        self.connection.commit()


    def create_user(self, user):
        self.cursor.execute('INSERT INTO users (name, email, password, banned) VALUES (%s, %s, %s, %s) RETURNING id', (user.username, user.email, user.password, user.banned))
        self.connection.commit()
        fetched = self.cursor.fetchone()
        user.set_user_id(fetched[0])
        return user

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

bg = BlogModel()
#bg.drop_table()
bg.create_table()
bg.check_user('admin', 'admin')