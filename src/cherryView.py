import cherrypy
# import model
import re
import authenticate
#db = model.BlogModel()


base_html = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: sans-serif;
        }
        h1 {
            text-align: center;
        }

    </style>
    <title>Bloggster</title>
</head>
<body>
    <h1>Bloggster</h1>
    <div>__CONTENT__</div>
</body>
</html>
'''

def post_to_html(posts):
    content = ''
    for post in posts:
        content += f'''
        <h2>{post[1]}</h2>
        <p>{post[2]}</p>
        '''

    return base_html.replace('__CONTENT__', content)

# create login function that returns form as string
def login():
    content = '''
    <form method="post" action="is_authenticated">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>
    '''
    return base_html.replace('__CONTENT__', content)

class BlogView(object):
    def __init__(self):
        self.posts = []

    def get_posts(self, posts):
        self.posts = posts

    @cherrypy.expose
    def index(self):
        html = login()
        return html

    @cherrypy.expose
    def main_page(self):
        return post_to_html(self.posts)

    @cherrypy.expose
    def is_authenticated(self, username=None, password=None):
        if authenticate.authenticate(username, password):
            # Authentication successful, render the main page
            return self.main_page()
        else:
            # Authentication failed, display an error message on the login page
            error_message = "Invalid username or password. Please try again."
            login_form = login() + f'<p style="color: red;">{error_message}</p>'
            return login_form
