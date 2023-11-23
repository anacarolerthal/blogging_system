#Data Layer - conexao com o banco
import psycopg2 

DATABASE_URL = "postgres://wxishrvi:2bKsBjBn5-hrqFKFb79grU1Kl71n9ext@isabelle.db.elephantsql.com/wxishrvi"

class BlogModel:
    def __init__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()

    def create_table(self):

        #User table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER serial PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                admin BOOLEAN DEFAULT FALSE
            )
        ''')

        #Post table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                post_id SERIAL PRIMARY KEY,
                author_id INTEGER REFERENCES users(user_id),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                title TEXT NOT NULL,
                content TEXT,
                image TEXT,
                parent_post_id INTEGER REFERENCES posts(id),
                CHECK (content IS NOT NULL OR image IS NOT NULL)
            )
        ''')

        #Tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                tag_id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        #Relation table for likes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS postLikes (
                like_id SERIAL PRIMARY KEY,
                post_id INTEGER REFERENCES posts(post_id),
                user_id INTEGER REFERENCES users(user_id),
                UNIQUE(post_id, user_id)
            )
        ''')

        #Relation table for followers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS userFollows (
                follow_id SERIAL PRIMARY KEY,
                follower_id INTEGER REFERENCES users(user_id),
                followee_id INTEGER REFERENCES users(user_id),
                UNIQUE(follower_id, followee_id)
            )
        ''')

        #Relation for banned users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bannedUsers (
                ban_id SERIAL PRIMARY KEY,
                banner_id INTEGER REFERENCES users(user_id),
                banned_id INTEGER REFERENCES users(user_id) UNIQUE
            )
        ''')

        #Relation for tags and posts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS postTags (
                tag_post_id SERIAL PRIMARY KEY,
                tag_id INTEGER REFERENCES tags(tag_id),
                post_id INTEGER REFERENCES posts(post_id),
                UNIQUE(tag_id, post_id)
            )
        ''')

        # create a new user
        self.cursor.execute('INSERT INTO users (name, email, password, admin) VALUES (%s, %s, %s, %s)', ('admin', 'admin', 'admin', True))

        self.connection.commit()

    def create_post(self, title, content):
        self.cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        self.connection.commit()

    def get_all_posts(self):
        self.cursor.execute('SELECT * FROM posts')
        return self.cursor.fetchall()