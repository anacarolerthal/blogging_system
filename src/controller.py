import model
import cherryView
import content
import cherrypy

class BlogController:
    def __init__(self, model, view_model):
        self.model = model
        self.view = view_model
        # self.post_factory = post_model.PostFactory()

    def create_post(self, post):
        self.model.create_post(post)

    def create_user(self, name, email):
        self.model.create_user(name, email)

    def show_page_n(self, page_num):
        posts = self.ContentModel.get_n_posts(20,offset=page_num)
        self.view.get_posts(posts)
        cherrypy.quickstart(self.view)

    def show_all_posts(self):
        posts = self.model.get_all_posts()
        self.view.get_posts(posts)
        cherrypy.quickstart(self.view)

    def login(self):
        username, password = self.view.login()
        self.model.check_user(username, password)

    def print_a(self):
        print('a')

if __name__ == '__main__':
    db = model.BlogModel()
    controller = BlogController(db, cherryView.BlogView())
    controller.show_all_posts()