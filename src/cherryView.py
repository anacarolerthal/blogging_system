import cherrypy
from admin import Admin

# read base_html file
with open('html/base_html.html', 'r') as f:
    base_html = f.read()


def post_to_html(posts):
    content = ''
    for post in posts:
        content += f'''
    <div class="blog-post">
        <div class="blog-post-title">{post[1]}</div>
        <div class="blog-post-content">
            <p>{post[2]}</p>
            <p>More content goes here...</p>
        </div>
        <div class="blog-post-meta">
            <span>Author: John Doe</span> |
            <span>Date: November 20, 2023</span>
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


    def get_posts(self, posts):
        self.posts = posts


    @cherrypy.expose
    def index(self):
        return login()


    @cherrypy.expose
    def main_page(self):
        return post_to_html(self.posts)


    @cherrypy.expose
    def is_authenticated(self, username=None, password=None):
        '''
        Function that authenticates a user
        '''
        admin = Admin()
        if admin.authenticate(username, password):
            # Authentication successful, render the main page
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
