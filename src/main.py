import model
import blog
import cherrypy

class BlogController:
    def __init__(self, model, view_model):
        self.model = model
        self.view = view_model

    def start(self):
        cherrypy.quickstart(self.view)

    # CODE SMELL

    # def create_post(self, post):
    #     self.model.create_post(post)

    # def create_user(self, name, email):
    #     self.model.create_user(name, email)

    # def show_page_n(self, page_num):
    #     posts = self.ContentModel.get_n_posts(20,offset=page_num)
    #     self.view.get_posts(posts)
    #     cherrypy.quickstart(self.view)

    # def login(self):
    #     username, password = self.view.login()
    #     self.model.check_user(username, password)

    # def register(self):
    #     username, password, email = self.view.register()
    #     self.model.create_user(username, password, email)


if __name__ == '__main__':
    db = model.BlogModel()
    controller = BlogController(db, blog.Blog())
    controller.start()