import cherrypy
from admin import Admin
from content import Post
from model import BlogModel
import utils

# read base_html file
with open('html/base_html.html', 'r') as f:
    base_html = f.read()


def post_to_html(posts):
    content = """
    <form method="post" action="create_post">
        <input type="text" name="title" placeholder="Sobre o que voce quer falar?">
        <input type="text" name="content" placeholder="Disserte sobre o assunto">
        <input type="submit" value="Postar">
    </form>    
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
            <span>Author: {post.author_id}</span> |
            <span>Date: {post.date}</span>
        </div>
    </div>
</body>
</html>
'''
    return base_html.replace('''</body>
</html>''', content)


def login():
    content = '''
    <form method="post" action="is_authenticated">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>
    Se você não tem uma conta, <a href="registering">registre-se</a>.
    </body>
</html>
    '''
    return base_html.replace('''</body>
</html>''', content)
    
    
def register():
    content = '''
    <form method="post" action="is_registered">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="email" name="email" placeholder="Email">
        <input type="submit" value="Register">
    </form>
    </body>
</html>
    '''
    return base_html.replace('''</body>
</html>''', content)


class BlogView(object):
    def __init__(self):
        self.posts = []
        self.model = BlogModel()

    @cherrypy.expose
    def index(self):
        return login()

    @cherrypy.expose
    def main_page(self):
        posts = [utils.transformPostDataToObject(post) for post in self.model.get_all_posts()]
        posts.reverse()
        self.posts = posts
        return post_to_html(self.posts)
    
    @cherrypy.expose
    def create_post(self, title, content):
        """
        Create a post and return to the all posts page
        """
        post = Post(
            author_id=user_id,
            title=title,
            content=content
        )

        id = post.publish()
        return self.main_page()


    @cherrypy.expose
    def is_authenticated(self, username=None, password=None):
        '''
        Function that authenticates a user
        '''
        admin = Admin()
        if admin.authenticate(username, password):
            # Authentication successful, render the main page
            global user_id
            user_id = admin.getId(username)
            return self.main_page()
        else:
            # Authentication failed, display an error message on the login page
            error_message = "Invalid username or password. Please try again."
            login_form = login() + f'<p style="color: red;">{error_message}</p>'
            return login_form
        
        
    @cherrypy.expose
    def registering(self):
        '''
        Function that renders the registration page
        '''
        return register()
        
        
    @cherrypy.expose
    def is_registered(self, username=None, password=None, email=None):
        '''
        Function that registers a user
        '''
        admin = Admin()
        print(admin.authenticate(username, password))
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
        print('a')
