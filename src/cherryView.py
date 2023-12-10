import cherrypy
from admin import Admin
from content import Post, Reply
from users import User
from tags import Tag
from model import BlogModel
import utils
import re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'html')
static_dir = os.path.abspath(static_dir)

cherrypy.config.update({
    'tools.staticdir.on': True,
    'tools.staticdir.dir': static_dir,
    'tools.staticdir.root': os.path.abspath(os.path.join(current_dir, '..'))
    })

# read base_html file
with open(os.path.join(static_dir, 'base_html.html'), 'r') as f:
    base_html = f.read()


def post_to_html(posts, user=None, n_followers=None, n_following=None):
    if user is not None and n_followers is not None and n_following is not None:
        user_id = user.get_id()
        content = f'''
        <div class="user-info">
            <h2>@username</h2>
            <h3>Seguidores: {n_followers} | Seguindo: {n_following} |  <a href="/followers_page/{user_id}">Ver</a></h3>
            <p>Deseja escrever uma <a href="http://localhost:8080/new_post">Nova Postagem</a>?</p>
        </div>
        '''
    else:
        content = """
        <h1 style="text-align: center;">Bem-vindo ao Bloggster!</h1>
        <p style="text-align: center;">Deseja escrever uma <a href="http://localhost:8080/new_post">Nova Postagem</a>?</p>  
        """

    for post in posts:
        content += f'''
    <div class="blog-post">
        <div class="blog-post-title">{post.title}</div>
        <div class="blog-post-content">
            <p>{post.content}</p>
            <p>More content goes here...</p>
        </div>
        <div class="blog-post-meta">
            <span>Author: <a href="users_page/{post.author_id}">{post.author_id}</a></span> |
            <span>Date: {post.date}</span>
            <span>Tags: {post.tags}</span>
        </div>
        <div class="blog-post-do-comment">
            <form method="post" action="do_comment" class="new-comment-form">
                <input type="hidden" name="post_id" value={post.id}>
                <textarea type="text" id="content" name="content" placeholder="Comente sobre" rows="4" required></textarea>
                <input type="submit" value="Comentar">
            </form>
            <form method="post" action="do_like">
                <input type="hidden" name="post_id" value={post.id}>
                <input type="submit" value="Like">
            </form>
        </div>
        <div class="blog-post-comments">
            Veja os <a href="get_post_comments/postId={post.id}">comentários</a>
        </div>
    </div>
</body>
</html>
'''
    return base_html.replace('''</body>
</html>''', content)

def new_post_to_html():
    # Renderiza a página para criar uma nova postagem
    content = """
    <form method="post" action="create_post" class="new-post-form">
        <label for="title">Título:</label>
        <input type="text" id="title" name="title" placeholder="Sobre o que voce quer falar?" required>

        <label for="content">Conteúdo:</label>
        <textarea type="text" id="content" name="content" placeholder="Disserte sobre o assunto" rows="15" required></textarea>

        <label for="tags">Tags:</label>
        <input type="text" name="tags" placeholder="Tags">

        <input type="submit" value="Postar">
    </form>
    """
    return base_html.replace('''</body>
</html>''', content)

def comments_to_html(comments):
    content = ''
    for comment in comments:
        content += f'''
        <div class="comment">
            <div class="comment-meta">
                <span>Author: {comment.author_id}</span> |
                <span>Date: {comment.date}</span>
            </div>
            <div class="comment-content">
                <p>{comment.content}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    content += '''<div class="back-button">
            <h2><a href="http://localhost:8080/main_page">← Voltar</a></h2>
        </div>'''
    return base_html.replace('''</body>
</html>''', content)

def login():
    content = '''
    <h1 style="text-align: center;">Login</h1>
    <form method="post" action="is_authenticated">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>
    <p style="text-align: center;">Se você ainda não tem uma conta, <a href="registering">registre-se</a>.</p>
    </body>
</html>
    '''
    return base_html.replace('''</body>
</html>''', content)

def register():
    content = '''
    <h1 style="text-align: center;">Registre-se</h1>
    <form method="post" action="is_registered">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="email" name="email" placeholder="Email">
        <input type="submit" value="Register">
    </form>
    <p style="text-align: center;">Já possui uma conta? Faça <a href="http://localhost:8080/">login</a>.</p>
    </body>
</html>
    '''
    return base_html.replace('''</body>
</html>''', content)

def personal_page_html(user, posts):
    followers = user.get_followers()
    following = user.get_following()

    return post_to_html(posts, user=user, n_followers=len(followers), n_following=len(following))

def followers_page_html(user, followers):
    content = f'''
    <div class="user-followers">
        <div class="followers-column">
            <h2>Seguidores:</h2>
            <ul>
            '''
    for follower in user.get_followers():
        content += f'<li>{follower}</li>'
    content += '''
            </ul>
        </div>
        <div class="following-column">
            <h2>Seguindo:</h2>
            <ul>
        '''
    for following in user.get_following():
        content += f'<li>{following}</li>'
    content += '''
            </ul>
        </div>
    </div>
    <br>
    <div class="back-button">
        <h2><a href="http://localhost:8080/users_page/'''+str(user.get_id())+'''">← Voltar</a></h2>
    </div>
    </body>
    </html>
        '''
    return base_html.replace('''</body>
</html>''', content)


class BlogView(object):
    def __init__(self):
        self.posts = []
        self.model = BlogModel()
        self.user_id = None

    @cherrypy.expose
    def index(self):
        return login()

    @cherrypy.expose
    def main_page(self):
        posts = [utils.transformPostDataToObject(post) for post in self.model.get_all_posts()]
        # get post tags
        tagged_posts =[]
        for post in posts:
            tag_ids = self.model.get_tags_for_post(post.id)
            print(tag_ids)
            # get tag names from tag ids
            tags = []
            for tag_id in tag_ids:
                tags.append(self.model.get_tag_name_by_id(tag_id))
            # add tags to post
            post.tags = tags
            tagged_posts.append(post)
        tagged_posts.reverse()
        self.posts = tagged_posts
        return post_to_html(self.posts)

    @cherrypy.expose
    def personal_page(self):
        if self.user_id is None:
            return login()
        # get user posts
        user_posts = [utils.transformPostDataToObject(post) for post in self.model.get_posts_for_user(self.user_id)]
        tagged_user_posts =[]
        # get post tags
        for post in user_posts:
            tag_ids = self.model.get_tags_for_post(post.id)
            # get tag names from tag ids
            tags = []
            for tag_id in tag_ids:
                tags.append(self.model.get_tag_name_by_id(tag_id))
            # add tags to post
            post.tags = tags
            tagged_user_posts.append(post)
        tagged_user_posts.reverse()
        
        # if user has no posts, display a message
        if len(tagged_user_posts) == 0:
            return personal_page_html(self.user, tagged_user_posts) + '<p style="text-align: center;">Você ainda não tem nenhuma postagem. Clique em <a href="http://localhost:8080/new_post">"Nova Postagem"</a> para começar a blogar!</p>'
        return personal_page_html(self.user, tagged_user_posts)
    
    @cherrypy.expose
    def followers_page(self, user_id):
        #if self.user_id is None:
        #    return login()
        username = self.model.get_username_by_user_id(int(user_id))
        # create user object
        user = User(
            username=username
        )
        user.set_id(int(user_id))
        # get user followers
        followers = user.get_followers()
        return followers_page_html(user, followers)

    @cherrypy.expose
    def users_page(self, author_id):
        username = self.model.get_username_by_user_id(int(author_id))
        # create user object
        some_other_user = User(
            username=username
        )
        some_other_user.set_id(int(author_id))
        # get user posts
        user_posts = [utils.transformPostDataToObject(post) for post in self.model.get_posts_for_user(author_id)]
        tagged_user_posts =[]
        # get post tags
        for post in user_posts:
            tag_ids = self.model.get_tags_for_post(post.id)
            # get tag names from tag ids
            tags = []
            for tag_id in tag_ids:
                tags.append(self.model.get_tag_name_by_id(tag_id))
            # add tags to post
            post.tags = tags
            tagged_user_posts.append(post)
        tagged_user_posts.reverse()
        return personal_page_html(some_other_user, tagged_user_posts)

    @cherrypy.expose
    def new_post(self):
        if self.user_id is None:
            return login()
        return new_post_to_html()

    @cherrypy.expose
    def create_post(self, title, content, tags):
        """
        Create a post and return to the all posts page
        """
        post_tags = []
        # for each word in tags, create a tag object and publish it
        for tag in tags.split():
            print(tag)
            tg = Tag(tag_name=tag)
            tg.publish()
            post_tags.append(tag)

        print(post_tags)
        
        post = Post(
            author_id=self.user_id,
            title=title,
            content=content,
            tags=post_tags
        )

        print(post.tags)

        post.publish()
        return self.main_page()

    @cherrypy.expose
    def is_authenticated(self, username=None, password=None):
        '''
        Function that authenticates a user
        '''
        admin = Admin()
        if admin.authenticate(username, password):
            # Authentication successful, render the main page
            self.user = User(
                username=username,
                password=password
            )
            user_id = self.model.get_user_id_by_username(username)
            self.user.set_id(user_id)
            self.user_id = self.user.get_id()
            return self.main_page()
        else:
            # Authentication failed, display an error message on the login page
            error_message = "Invalid username or password. Please try again."
            login_form = login() + f'<p style="color: red; text-align:center;">{error_message}</p>'
            return login_form

    @cherrypy.expose
    def registering(self):
        '''
        Function that renders the registration page
        '''
        return register()

    @cherrypy.expose
    def do_comment(self, content, post_id):
        reply = Reply(
            author_id=self.user_id,
            content=content,
            parent_post_id=post_id
        )
        query_string = "postId="+post_id
        id = reply.publish()
        return self.get_post_comments(query_string)

    @cherrypy.expose
    def get_post_comments(self, postId):
        pattern = r'(?<==)([^=\s]+)' #The "postId" parameter is in the format "postId=8", so use regex to extract the 8
        matches = re.findall(pattern, postId)
        id = int(matches[0])
        comments = self.model.get_comments_for_post(id)
        if len(comments) > 0:
            comments = [utils.transformReplyDataToObject(reply) for reply in comments]
            comments.reverse()
            return comments_to_html(comments)
        else:
            return comments_to_html([]) + f'<p style="text-align: center;">Ainda não há comentários. Seja o primeiro a comentar!</p>'

    @cherrypy.expose
    def do_like(self, post_id):
        try:
            self.user.like(post_id)
            return self.main_page().replace('''<input type="submit" value="Like">''',
                                            '''<input type="submit" value="Unlike">''')
        except Exception as e:
            # dislike
            self.user.unlike(post_id)
            return self.main_page()

    @cherrypy.expose
    def is_registered(self, username=None, password=None, email=None):
        '''
        Function that registers a user
        '''
        admin = Admin()
        if not admin.authenticate(username, password):
            admin.register(username, password, email)
            # redirect to login page
            return login() + '<p style="color: green;">Registrado com sucesso! Faça login.</p>'
        else:
            # Registration failed, display an error message on the registration page
            error_message = "Nome de usuário em uso. Por favor, tente novamente."
            register_form = register() + f'<p style="color: red;">{error_message}</p>'
            return register_form

    @cherrypy.expose
    def print_a(self):
        print('.')