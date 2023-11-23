from model import BlogModel
from controller import BlogController
import cherryView

if __name__ == "__main__":
    model = BlogModel()
    view = cherryView.BlogView()
    controller = BlogController(model, view)

    # Create a new post
    controller.create_post("Title 1", "Content of post 1")

    # Display all posts
    controller.show_all_posts()