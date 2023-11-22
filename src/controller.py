import model
import cherryView
import post_model
import cherrypy

class BlogController:
    def __init__(self, model, view_model):
        self.model = model
        self.view = view_model
        self.post_factory = post_model.PostFactory()

    def create_post(self, title, content):
        self.model.create_post(title, content)

    def show_all_posts(self):
        posts = self.model.get_all_posts()
        self.view.get_posts(posts)
        cherrypy.quickstart(self.view)

    def login(self):
        username, password = self.view.login()
        self.model.check_user(username, password)


if __name__ == '__main__':
    db = model.BlogModel()
    db.create_table()
    controller = BlogController(db, cherryView.BlogView())
    controller.show_all_posts()