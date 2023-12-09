import cherrypy
from admin import Admin
from content import Post, Reply
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
    })

# read base_html file
with open('src/html/base_html.html', 'r') as f:
    base_html = f.read()


def post_to_html(posts):
    # Renderiza a página principal
    content = ''
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
        <div class="blog-post-do-comment">
            <form method="post" action="do_comment" class="new-comment-form">
                <input type="hidden" name="post_id" value={post.id}>
                <textarea type="text" id="content" name="content" placeholder="Comente sobre" rows="4" required></textarea>
                <input type="submit" value="Comentar">
            </form>
        </div>
        <div class="blog-post-comments">
            Veja os <a href="get_post_comments/postId={post.id}">comentarios</a>
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
        <textarea type="text" id="content" name="content" placeholder="Disserte sobre o assunto" rows="10" required></textarea>

        <label for="tags">Tags:</label>

        <input type="submit" value="Postar">
    </form>    
    """
    return base_html.replace('''</body>
</html>''', content)

def comments_to_html(comments):
    content = ''
    for comment in comments:
        content += f'''
        <div class="comment-meta">
            <span>Author: {comment.author_id}</span> |
            <span>Date: {comment.date}</span>
        </div>
    <div class="comment">
        <div class="comment-content">
            <p>{comment.content}</p>
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
    <p style="text-align: center;">Se você ainda não tem uma conta, <a href="registering">registre-se</a>.</p>
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
    <p style="text-align: center;">Já possui uma conta? Faça <a href="http://localhost:8080/">login</a>.</p>
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
        posts.reverse()
        self.posts = posts
        return post_to_html(self.posts)
    
    @cherrypy.expose
    def my_posts(self):
        posts = [utils.transformPostDataToObject(post) for post in self.model.get_posts_by_author(self.user_id)]
        posts.reverse()
        self.posts = posts
        # se o usuario nao tiver posts, exibe uma mensagem
        if len(posts) == 0:
            content = '''<p>Você ainda não tem posts publicados. Vá em <a href=http://localhost:8080/new_post>Escrever novo post</a> para começar a blogar!</p>'''
            return base_html.replace('''</body>
                                     </html>''', content)
        return post_to_html(self.posts)
    
    @cherrypy.expose
    def new_post(self):
        return new_post_to_html()
    
    @cherrypy.expose
    def create_post(self, title, content):
        """
        Create a post and return to the all posts page
        """
        post = Post(
            author_id=self.user_id,
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
            self.user_id = admin.getId(username)
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
        if comments is not None:
            comments = [utils.transformReplyDataToObject(reply) for reply in comments]
            comments.reverse()
            return comments_to_html(comments)  
        else:
            return "Nao ha comentarios"
        
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
