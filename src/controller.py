class BlogController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_post(self, title, content):
        self.model.create_post(title, content)

    def show_all_posts(self):
        posts = self.model.get_all_posts()
        self.view.show_all_posts(posts)