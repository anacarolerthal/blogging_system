import cherrypy
from admin import Admin
from users import UserFactory
from model import BlogModel
from customExceptions import *
import refacFunctions as rf
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'html')
static_dir = os.path.abspath(static_dir)

cherrypy.config.update({
    'tools.staticdir.on': True,
    'tools.staticdir.dir': static_dir,
    'tools.staticdir.root': os.path.abspath(os.path.join(current_dir, '..'))
    })

# read index_html file
with open(os.path.join(static_dir, 'index_html.html'), 'r') as f:
    index_html = f.read()

# read base_html file
with open(os.path.join(static_dir, 'base_html.html'), 'r') as f:
    base_html = f.read()

# read base_moderator file
with open(os.path.join(static_dir, 'base_moderator.html'), 'r') as f:
    base_moderator = f.read()


def post_to_html(posts, user=None, n_followers=None, n_following=None, logged_user=None):
    if user is not None and n_followers is not None and n_following is not None:
        user_id = user.get_id()
        user_name = user.get_username()
        content = f'''
            <div class="user-info">
                <h2>@{user_name}</h2>
                <h3>Seguidores: {n_followers} | Seguindo: {n_following} |  <a href="/followers_page/{user_id}">Ver</a></h3>
            '''
        if logged_user is not None:
            if user_id in logged_user.get_following():
                updated_button = "Deixar de Seguir"
            else:
                updated_button = "Seguir"
            content += f'''
                <form method="post" action="/do_follow" class="follow-form" id="follow-form" data-user-id="{user_id}">
                    <input type="hidden" name="user_id" value={user_id}>
                    <input type="submit" class="follow-button" id="followButton{user_id}" value="{updated_button}">
                </form>
            </div>
            <div class="back-button" style="margin-left: 145px;">
            <h3><a href="http://localhost:8080/main_page">← Voltar</a></h3>
            </div>
            '''
        else:
            content += '''</div>'''
    else:
        content = """
        <h1 style="text-align: center;">Bem-vindo ao Bloggster!</h1>
        <p style="text-align: center;">Deseja escrever uma <a href="http://localhost:8080/new_post">Nova Postagem</a>?</p>
        """

    for post in posts:
        # get author username
        author_id = post.author_id
        author_username = BlogModel().get_username_by_user_id(author_id)

        content += f'''
        <div class="blog-post">
            <div class="blog-post-title">{post.title}</div>
            <div class="blog-post-content">
                <p>{post.content}</p>
            </div>
            <div class="blog-post-meta">
                <span>Autor: <a href="users_page/{post.author_id}">{author_username}</a></span> |
                <span>Data: {post.date}</span> |
                <span>Tags: {post.tags}</span>
            </div>
            <div class="blog-post-do-comment">
                <form method="post" action="do_comment" class="new-comment-form">
                    <input type="hidden" name="post_id" value={post.id}>
                    <textarea type="text" id="content" name="content" placeholder="Comente sobre" rows="4" required></textarea>
                    <input type="submit" value="Comentar">
                </form>
            </div>
            <div class="blog-post-likes">
                <form method="post" action="do_like" class="like-form" id="like-form" data-post-id="{post.id}">
                    <input type="hidden" name="post_id" value={post.id}>
                    <input type="submit" class="like-button" id="likeButton{post.id}" value="Like">
                </form>
            </div>
            <div class="blog-post-comments">
                Veja os <a href="get_post_comments/postId={post.id}">comentários</a>
            </div>
        </div>
    </body>
    '''
    return base_html.replace('''</body>''', content)

def moderator_post_to_html(posts, user=None):
    content = ''
    if user is not None:
        user_id = user.get_id()
        user_name = user.get_username()

        # check if user_id is banned
        is_banned = BlogModel().check_if_user_is_banned(user_id)

        if is_banned:
            updated_button = "Desbanir"
        else:
            updated_button = "Banir"
        content = f'''
            <div class="user-info">
                <h2>@{user_name}</h2>
            </div>
            <form method="post" action="/do_ban" class="ban-form" id="ban-form" data-user-id="{user_id}">
                <input type="hidden" name="user_id" value={user_id}>
                <input type="submit" class="ban-button" id="banButton{user_id}" value="{updated_button}">
            </form>

            <div class="back-button" style="margin-left: 145px;">
            <h3><a href="http://localhost:8080/main_page">← Voltar</a></h3>
            </div>
            '''

    content+= """
    <h1 style="text-align: center;">Bem-vindo ao Bloggster, moderador!</h1>
    """
    for post in posts:
        # get author username
        author_id = post.author_id
        author_username = BlogModel().get_username_by_user_id(author_id)

        content += f'''
    <div class="blog-post">
        <div class="blog-post-title">{post.title}</div>
        <div class="blog-post-content">
            <p>{post.content}</p>
            <p>More content goes here...</p>
        </div>
        <div class="blog-post-meta">
            <span>Author: <a href="users_page/{post.author_id}">{author_username}</a></span> |
            <span>Date: {post.date}</span>
            <span>Tags: {post.tags}</span>
        </div>
        <div class="blog-post-delete">
            <form method="post" action="delete_post" class="delete-post-form">
                <input type="hidden" name="post_id" value={post.id}>
                <input type="submit" value="Delete">
            </form>
        </div>
        <div class="blog-post-comments">
            Veja os <a href="get_post_comments/postId={post.id}">comentários</a>
        </div>
    </div>
</body>
'''
    return base_moderator.replace('''</body>''', content)

def new_post_to_html():
    # Renderiza a página para criar uma nova postagem
    content = """
    <form method="post" action="create_post" class="new-post-form">
        <label for="title">Título:</label>
        <input type="text" id="title" name="title" placeholder="Sobre o que voce quer falar?" required>

        <label for="content">Conteúdo:</label>
        <textarea type="text" id="content" name="content" placeholder="Disserte sobre o assunto" rows="15" required></textarea>

        <label for="tags">Tags:</label>
        <input type="text" name="tags" placeholder="Separe as Tags por espaço">

        <input type="submit" value="Postar">
    </form>
    </body>
    """
    return base_html.replace('''</body>''', content)

def comments_to_html(comments, is_moderator= False):
    content = ''
    for comment in comments:
        content += f'''
        <div class="comment">
            <div class="comment-meta">
                <span>Autor: {comment.author_id}</span> |
                <span>Data: {comment.date}</span>
            </div>
            <div class="comment-content">
                <p>{comment.content}</p>
            </div>
        </div>
    </body>
    '''
    content += '''<div class="back-button">
            <h2><a href="http://localhost:8080/main_page">← Voltar</a></h2>
        </div>'''
    if is_moderator:
        return base_moderator.replace('''</body>''', content)
    return base_html.replace('''</body>''', content)

def tag_search_html(is_moderator=False):
    content = '''
    <!-- <h1 style="text-align: center;">Search by tag</h1> -->
    <h1 style="text-align: center;">Filtrar por tag</h1>
    <form method="post" action="tag_search_result">
        <input type="text" name="tag" placeholder="Tag">
        <!-- <input type="submit" value="Search"> -->
        <input type="submit" value="Filtrar">
    </form>
    </body>
    '''
    if is_moderator:
        return base_moderator.replace('''</body>''', content)
    return base_html.replace('''</body>''', content)

def tag_search_result_html(posts, is_moderator=False):
    content = '''
    <!-- <h1 style="text-align: center;">Search by tag</h1> -->
    <h1 style="text-align: center;">Filtrar por tag</h1>
    <form method="post" action="tag_search_result">
        <input type="text" name="tag" placeholder="Tag">
        <!-- <input type="submit" value="Search"> -->
        <input type="submit" value="Filtrar">
    </form>
    '''
    for post in posts:
        # get author username
        author_username = BlogModel().get_username_by_user_id(post.author_id)
        content += f'''
    <div class="blog-post">
        <div class="blog-post-title">{post.title}</div>
        <div class="blog-post-content">
            <p>{post.content}</p>
        </div>
        <div class="blog-post-meta">
            <!-- <span>Autor: {post.author_id}</span> | -->
            <span>Autor: <a href="users_page/{post.author_id}">{author_username}</a></span> |
            <span>Data: {post.date}</span> |
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
'''
    if is_moderator:
        return base_moderator.replace('''</body>''', content)
    return base_html.replace('''</body>''', content)

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
    '''
    return index_html.replace('''</body>''', content)

def register():
    content = '''
    <h1 style="text-align: center;">Registre-se</h1>
    <form method="post" action="is_registered">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="email" name="email" placeholder="Email">
        <label for="is_moderator">Moderador?</label>
        <input type="checkbox" name="is_moderator" value="True">
        <input type="submit" value="Register">
    </form>
    <p style="text-align: center;">Já possui uma conta? Faça <a href="http://localhost:8080/">login</a>.</p>
    </body>
    '''
    return index_html.replace('''</body>''', content)

def personal_page_html(user, posts, logged_user=None, is_moderator=False):
    if is_moderator:
        return moderator_post_to_html(posts, user = user)
    followers = user.get_followers()
    following = user.get_following()
    return post_to_html(posts, user=user, n_followers=len(followers), n_following=len(following), logged_user=logged_user)

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
        '''
    return base_html.replace('''</body>''', content)


class Blog(object):
    def __init__(self):
        self.posts = []
        self.model = BlogModel()
        self.user_id = None
        self.user = None

    @cherrypy.expose
    def index(self):
        if self.user is not None:
            self.user.logout()
        return login()

    # OLD VERSION OF main_page
    # @cherrypy.expose
    # def main_page(self):
    #     posts = [utils.transformPostDataToObject(post) for post in self.model.get_all_posts()]
    #     # get post tags
    #     tagged_posts =[]
    #     for post in posts:
    #         tag_ids = self.model.get_tags_for_post(post.id)
    #         # get tag names from tag ids
    #         tags = []
    #         for tag_id in tag_ids:
    #             if tag_id is not None:
    #                 tags.append(self.model.get_tag_name_by_id(tag_id))
    #         # add tags to post
    #         post.tags = tags
    #         tagged_posts.append(post)
    #     tagged_posts.reverse()
    #     self.posts = tagged_posts
    #     if self.is_moderator:
    #         return moderator_post_to_html(self.posts)
    #     elif not self.is_moderator:
    #         return post_to_html(self.posts)
    
    # REFACTORED VERSION OF main_page
    @cherrypy.expose
    def main_page(self):
        if self.user.is_logged_in():
          tagged_posts = rf.getTaggedPosts(self.model)
          self.posts = tagged_posts

          if self.is_moderator:
              return moderator_post_to_html(self.posts)
          elif not self.is_moderator:
              return post_to_html(self.posts)
        else:
            return login()
    
    # # OLD VERSION OF personal_page
    # @cherrypy.expose
    # def personal_page(self):
    #     if self.user_id is None:
    #         return login()
    #     # get user posts
    #     user_posts = [utils.transformPostDataToObject(post) for post in self.model.get_posts_for_user(self.user_id)]
    #     tagged_user_posts =[]
    #     # get post tags
    #     for post in user_posts:
    #         tag_ids = self.model.get_tags_for_post(post.id)
    #         # get tag names from tag ids
    #         tags = []
    #         for tag_id in tag_ids:
    #             if tag_id is not None:
    #                 tags.append(self.model.get_tag_name_by_id(tag_id))
    #         # add tags to post
    #         post.tags = tags
    #         tagged_user_posts.append(post)
    #     tagged_user_posts.reverse()
        
    #     # if user has no posts, display a message
    #     if len(tagged_user_posts) == 0:
    #         return personal_page_html(self.user, tagged_user_posts, self.user, self.is_moderator) + '<p style="text-align: center;">Você ainda não tem nenhuma postagem. Clique em <a href="http://localhost:8080/new_post">"Nova Postagem"</a> para começar a blogar!</p>'
    #     return personal_page_html(self.user, tagged_user_posts, self.user, self.is_moderator)
    
    # REFACTORED VERSION OF personal_page
    @cherrypy.expose
    def personal_page(self):
        if self.user.is_logged_in():
          tagged_user_posts = rf.getTaggedPosts(self.model, self.user_id)
          # if user has no posts, display a message
          if len(tagged_user_posts) == 0:
              return personal_page_html(self.user, tagged_user_posts, self.user, self.is_moderator) + '<p style="text-align: center;">Você ainda não tem nenhuma postagem. Clique em <a href="http://localhost:8080/new_post">"Nova Postagem"</a> para começar a blogar!</p>'
          return personal_page_html(self.user, tagged_user_posts, self.user, self.is_moderator)
        else:
            return login()

    @cherrypy.expose
    def tags_filter(self):
        if self.user.is_logged_in():
            return tag_search_html(self.is_moderator)
        else:
            return login()
    
    # OLD VERSION OF tag_search_result
    # @cherrypy.expose
    # def tag_search_result(self, tag):
    #     # check if tag exists
    #     if not self.model.check_if_tag_in_db(tag):
    #         return tag_search_result_html([])
    #     # get tag id from tag name
    #     tag_id = self.model.get_tag_id_by_name(tag)
    #     post_ids = self.model.get_post_id_by_tag(tag_id)
    #     # for each post id, get post data
    #     posts = []
    #     for post_id in post_ids:
    #         posts.append(utils.transformPostDataToObject(self.model.get_post_by_post_id(post_id)))
    #     tagged_posts =[]
    #     # get post tags
    #     for post in posts:
    #         tag_ids = self.model.get_tags_for_post(post.id)
    #         # get tag names from tag ids
    #         tags = []
    #         for tag_id in tag_ids:
    #             if tag_id is not None:
    #                 tags.append(self.model.get_tag_name_by_id(tag_id))
    #         # add tags to post
    #         post.tags = tags
    #         tagged_posts.append(post)
    #     tagged_posts.reverse()
    #     return tag_search_result_html(tagged_posts, self.is_moderator)
    
    # REFACTORED VERSION OF tag_search_result
    @cherrypy.expose
    def tag_search_result(self, tag):
        if self.user.is_logged_in():
        # check if tag exists
          if not self.model.check_if_tag_in_db(tag):
            return tag_search_result_html([])
          posts = rf.getPostsByPostID(self.model, tag)
          return tag_search_result_html(posts, self.is_moderator)
        else:
            return login()


    # OLD VERSION OF followers_page
    # @cherrypy.expose
    # def followers_page(self, user_id):
    #     #if self.user_id is None:
    #     #    return login()
    #     username = self.model.get_username_by_user_id(int(user_id))
    #     # create user object
    #     user = User(
    #         username=username
    #     )
    #     user.set_id(int(user_id))
    #     # get user followers
    #     followers = user.get_followers()
    #     return followers_page_html(user, followers)
    
    # REFACTORED VERSION OF followers_page
    @cherrypy.expose
    def followers_page(self, user_id):
        #if self.user_id is None:
        #    return login()
        if self.user.is_logged_in():
          user, followers = rf.getUserFollowers(self.model, user_id)
          return followers_page_html(user, followers)
        else:
            return login()

    # OLD VERSION OF users_page
    # @cherrypy.expose
    # def users_page(self, author_id):
    #     username = self.model.get_username_by_user_id(int(author_id))
    #     # create user object
    #     # some_other_user = User(
    #     #     username=username
    #     # )
    #     some_other_user = UserFactory().create_user("USER", username, author_id)
    #     some_other_user.set_id(int(author_id))
    #     # get user posts
    #     user_posts = [utils.transformPostDataToObject(post) for post in self.model.get_posts_for_user(author_id)]
    #     tagged_user_posts =[]
    #     # get post tags
    #     for post in user_posts:
    #         tag_ids = self.model.get_tags_for_post(post.id)
    #         # get tag names from tag ids
    #         tags = []
    #         for tag_id in tag_ids:
    #             if tag_id is not None:
    #                 tags.append(self.model.get_tag_name_by_id(tag_id))
    #         # add tags to post
    #         post.tags = tags
    #         tagged_user_posts.append(post)
    #     tagged_user_posts.reverse()
    #     return personal_page_html(some_other_user, tagged_user_posts, self.user, self.is_moderator)
    
    # REFACTORED VERSION OF users_page
    @cherrypy.expose
    def users_page(self, author_id):
        if self.user.is_logged_in():
          username = self.model.get_username_by_user_id(int(author_id))
          some_other_user = UserFactory().create_user("USER", username, author_id)
          some_other_user.set_id(int(author_id))
          tagged_user_posts = rf.getTaggedPosts(self.model, author_id)
          return personal_page_html(some_other_user, tagged_user_posts, self.user, self.is_moderator)           
        else:
            return login()

    @cherrypy.expose
    def new_post(self):
        #if self.user_id is None:
        #    return login()
        if self.user.is_logged_in():
            return new_post_to_html()
        else:
            return login()

    # OLD VERSION OF create_post
    # @cherrypy.expose
    # def create_post(self, title, content, tags):
    #     """
    #     Create a post and return to the all posts page
    #     """
    #     post_tags = []
    #     # for each word in tags, create a tag object and publish it
    #     for tag in tags.split():
    #         tg = Tag(tag_name=tag)
    #         tg.publish()
    #         post_tags.append(tag)

    #     post = Post(
    #         author_id=self.user_id,
    #         title=title,
    #         content=content,
    #         tags=post_tags
    #     )

    #     post.publish()
    #     return self.main_page()

    # REFACTORED VERSION OF create_post
    @cherrypy.expose
    def create_post(self, title, content, tags):
        """
        Create a post and return to the all posts page
        """
        if self.user.is_logged_in():
            post_tags = rf.splitTags(tags)
            post = rf.createPostWithSplitTags(self.user_id, title, content, post_tags)
            post.publish()
            return self.main_page()
        else:
            return login()

    #OLD VERSION OF is_authenticated
    @cherrypy.expose
    def is_authenticated(self, username=None, password=None):
        '''
        Function that authenticates a user
        '''
        admin = Admin()
        if admin.authenticate(username, password):
            # Authentication successful, render the main page
            self.is_moderator = admin.is_moderator(username)
            user_id = self.model.get_user_id_by_username(username)
            if self.is_moderator:
                self.user = UserFactory().create_user("MODERATOR", username, user_id)
            elif not admin.is_moderator(username):
                self.user = UserFactory().create_user("USER", username, user_id)
                if (BlogModel().check_if_user_is_banned(user_id)):
                    return login() + '<p style="color: red; text-align: center;">Você está banido.</p>'
            self.user.login()
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

    # OLD VERSION OF do_reply
    # @cherrypy.expose
    # def do_comment(self, content, post_id):
    #     reply = Reply(
    #         author_id=self.user_id,
    #         content=content,
    #         parent_post_id=post_id
    #     )
    #     query_string = "postId="+post_id
    #     id = reply.publish()
    #     return self.get_post_comments(query_string)
    
    # REFACTORED VERSION OF do_comment
    @cherrypy.expose
    def do_comment(self, content, post_id):
        if self.user.is_logged_in():
            reply, query_string = rf.createReplyWithPostID(self.user_id, post_id, content)
            reply.publish()
            return self.get_post_comments(query_string)
        else:
            return login()
          
    @cherrypy.expose
    def do_follow(self, user_id):
        if self.user.is_logged_in():
            try:
                self.user.follow(int(user_id))
                # return to that user's page
                #return self.users_page(int(user_id))
                updated_button = "Deixar de Seguir"
                success = True
                user_url = f'/users_page/{user_id}'
            except AlreadyFollowing as e:
                # unfollow
                #self.user.unfollow(int(user_id))
                #return self.users_page(int(user_id))
                self.user.unfollow(int(user_id))
                updated_button = "Seguir"
                success = True
                user_url = f'/users_page/{user_id}'
            except FollowInvalidUser as e:
                # invalid user
                return self.users_page(int(user_id))
            except CannotFollowSelf as e:
                # cannot follow self 
                # add message to page
                return self.users_page(int(user_id)) + '<p style="text-align: center;">Não é possível seguir a si mesmo.</p>'
            return json.dumps({'success': success, 'updated_button': updated_button, 'user_url': user_url})
        else:
            return login()
    
    @cherrypy.expose
    def do_ban(self, user_id):
        if self.user.is_logged_in():
            try:
                # insert ban in database
                self.user.ban_user(int(user_id))
                updated_button = "Desbanir"
                success = True
                user_url = f'/users_page/{user_id}'
            except AlreadyBanned as e:
                # remove ban
                self.user.unban_user(int(user_id))
                updated_button = "Banir"
                success = True
                user_url = f'/users_page/{user_id}'
            except InvalidUserException as e:
                # invalid user
                return self.users_page(int(user_id)) + '<p style="text-align: center;">Usuário inválido.</p>'
            return json.dumps({'success': success, 'updated_button': updated_button, 'user_url': user_url})
        else:
            return login()
          
    # OLD VERSION OF get_post_comments
    # @cherrypy.expose
    # def get_post_comments(self, postId):
    #     pattern = r'(?<==)([^=\s]+)' #The "postId" parameter is in the format "postId=8", so use regex to extract the 8
    #     matches = re.findall(pattern, postId)
    #     id = int(matches[0])
    #     comments = self.model.get_comments_for_post(id)
    #     if len(comments) > 0:
    #         comments = [utils.transformReplyDataToObject(reply) for reply in comments]
    #         comments.reverse()
    #         return comments_to_html(comments, self.is_moderator)
    #     else:
    #         return comments_to_html([], self.is_moderator) + f'<p style="text-align: center;">Ainda não há comentários.</p>'
    
    # REFACTORED VERSION OF get_post_comments
    @cherrypy.expose
    def get_post_comments(self, postId):
        if self.user.is_logged_in():
            comments = rf.getComments(self.model, postId)
            if len(comments) > 0:
                comments = rf.getCommentsObjects(comments)
                return comments_to_html(comments, self.is_moderator)
            else:
                return comments_to_html([], self.is_moderator) + f'<p style="text-align: center;">Ainda não há comentários.</p>'
        else:
            return login()

    @cherrypy.expose
    def do_like(self, post_id):
        if self.user.is_logged_in():
            try:
                self.user.like(post_id)
                # like
                updated_button = "Unlike"
                success = True
            except Exception as e:
                # dislike
                self.user.unlike(post_id)
                updated_button = "Like"
                success = True
            return json.dumps({'success': success, 'updated_button': updated_button})
        else:
            return login()
    
    @cherrypy.expose
    def delete_post(self, post_id):
      if self.user.is_logged_in():
            try:
                self.user.delete_post(post_id)
                return self.main_page()
            except InvalidPostException as e:
                # invalid post
                return self.main_page() + '<p style="text-align: center;">Post inválido.</p>'
      else:
          return login()  

    @cherrypy.expose
    def is_registered(self, username=None, password=None, email=None, is_moderator=None):
        '''
        Function that registers a user
        '''
        admin = Admin()
        if not admin.authenticate(username, password):
            if is_moderator == "True":
                is_moderator = True
            else:
                is_moderator = False

            admin.register(username, password, email, is_moderator)
            # redirect to login page
            return login() + '<p style="color: green; text-align: center;">Registrado com sucesso! Faça login.</p>'
        else:
            # Registration failed, display an error message on the registration page
            error_message = "Nome de usuário em uso. Por favor, tente novamente."
            register_form = register() + f'<p style="color: red; text-align: center;">{error_message}</p>'
            return register_form

    @cherrypy.expose
    def print_a(self):
        print('.')