import unittest
import sys

#APPENDS SRC FOLDER TO PATH
sys.path.append('./src')

from users import User, Moderator
from content import Post, Reply

class TestPostSystem(unittest.TestCase):
    def setUp(self):
        # Initialize objects for testing
        # arrange
        self.post = Post(id = 1, author_id = 1,  date = "1999-01-01 12:04:16", title="Title", content="This is a test post.", tags=['tag10','tag20'])
        self.reply = Reply(id = 1, author_id = 1, date = "1999-01-01 12:04:18", parent_post_id = 1, content="This is a test comment.")
        self.user = User(id=1, username="user1", password="pass1", email="email@email.com")

    # TESTING GETTER
    def test_post_get_id(self):
        # act
        post_id = self.post.get_id()

        #assert
        self.assertIsInstance(post_id, int)

    def test_post_get_author_id(self):
        # act
        post_author_id = self.post.get_author_id()

        #assert
        self.assertIsInstance(post_author_id, int)

    def test_post_get_date(self):
        # act
        post_date = self.post.get_date()

        # assert
        self.assertIsInstance(post_date, str)

    def test_post_get_title(self):
        # act
        post_title = self.post.get_title()

        # assert
        self.assertIsInstance(post_title, str)

    def test_post_get_content(self):
        # act
        post_content = self.post.get_content()

        # assert
        self.assertIsInstance(post_content, str)

    def test_post_get_tags(self):
        # act
        post_tags = self.post.get_tags()

        # assert
        self.assertIsInstance(post_tags, list)

    # TESTING SETTERS
    def test_post_set_id(self):
        # arrange
        self.post.set_id(2)

        # act
        this_post_id = self.post.get_id()

        # assert
        self.assertEqual(this_post_id, 2)

    def test_post_set_invalid_id(self):
        # arrange
        post_Id = None

        # act
        with self.assertRaises(TypeError) as context:
            self.post.set_id(post_Id)

        # assert
        self.assertEqual("Tipo inválido de id. Ids devem ser inteiros." , str(context.exception))


    def test_post_set_date(self):
        # arrange
        self.post.set_date("1999-01-01 12:04:16")

        # act
        this_post_date = self.post.get_date()

        # assert
        self.assertEqual(this_post_date, "1999-01-01 12:04:16")

    def test_post_set_invalid_date(self):
        # arrange
        post_date = None

        # act
        with self.assertRaises(TypeError) as context:
            self.post.set_date(post_date)

        # assert
        self.assertEqual("Tipo inválido para data. Ids devem ser Strings na forma 'YYYY-mm-dd hh:mm:ss'." , str(context.exception))

    def test_post_publish(self):
        # arrange
        self.post.publish()

        # act
        this_post_id = self.post.get_id()

        # assert
        self.assertIsInstance(this_post_id, int)

    def test_post_render(self):
        # arrange
        self.post.publish()

        # act
        this_post_render = self.post.render()

        # assert
        self.assertIsInstance(this_post_render, str)

    def test_post_publish_tags(self):
        # arrange

        self.post.publish_tags()

        # act
        this_post_tags = self.post.get_tags()

        # assert
        self.assertIsInstance(this_post_tags, list)


if __name__ == '__main__':
    unittest.main()
