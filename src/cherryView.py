import cherrypy
#import model
import re
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



class BlogView(object):
    def get_posts(self,posts):
        self.posts = posts
    @cherrypy.expose
    def index(self):
        html = post_to_html(self.posts)
        return html
