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
        .blog-post {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .blog-post-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }

        .blog-post-content {
            margin-top: 10px;
            color: #666;
        }

        .blog-post-meta {
            margin-top: 15px;
            color: #888;
        }
    </style>

    <script>
    // Function to check if the user has scrolled to the bottom
    function isScrolledToBottom() {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
      const clientHeight = document.documentElement.clientHeight || document.body.clientHeight;
      return scrollTop + clientHeight >= scrollHeight;
    }

    

    // Event listener for scrolling
    window.addEventListener('scroll', function () {
      if (isScrolledToBottom()) {
        alert('You scrolled to the bottom!');
        window.location.href = "http://localhost:8080/print_a";
        //window.location.href = "http://localhost:8080/page2";

      }
    });
    </script>

    <title>Bloggster</title>
</head>
<body>
    <h1>Bloggster</h1>

</body>
</html>
'''

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

class BlogView(object):
    def get_posts(self,posts):
        self.posts = posts
    @cherrypy.expose
    def index(self):
        html = post_to_html(self.posts)
        return html
    @cherrypy.expose
    def print_a(self):
        print('a')
    
    #make a multipage feed