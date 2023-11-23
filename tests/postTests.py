import unittest
import sys

sys.path.append('../')
from src.users import User, Moderator
from src.posts import Post, Comment

class TestPostSystem(unittest.TestCase):
    def setUp(self):
        # Initialize objects for testing
        self.post = Post(title="Title", content="This is a test post.", author_id = 1, id = 1, comments = [], date = "1999-01-01 12:04:16")
        self.comment = Comment(content="This is a test comment.", author_id = 1, id = 2, parent_post_id = 1, date = "1999-01-01 12:04:18")
        self.user = User(username="user1", password="pass1", email="email@email.com")

    # TESTING GETTERS
    def test_post_get_title(self):
        self.assertIsInstance(self.post.get_title(), str)
    
    def test_post_get_content(self):
        self.assertIsInstance(self.post.get_content(), str)
    
    def test_post_get_author_id(self):
        self.assertIsInstance(self.post.get_author_id(), int)
    
    def test_post_get_id(self):
        self.assertIsInstance(self.post.get_id(), int)

    def test_post_get_comments(self):
        self.assertIsInstance(self.post.get_comments(), list)
    
    # TESTING SETTERS
    def test_post_set_id(self):
        self.post.set_id(2)
        self.assertEqual(self.post.get_id(), 2)

    def test_post_set_invalid_id(self):
        postId = None
        self.assertRaises(self.post.set_id(postId), "InvalidFunctionArguments")
        
    def test_post_set_date(self):
        self.post.set_date("1999-01-01 12:04:16")
        self.assertEqual(self.post.get_date(), "1999-01-01 12:04:16")
    
    def test_post_set_invalid_date(self):
        date = None
        self.assertRaises(self.post.set_date(date), "InvalidFunctionArguments")
    
    # TESTING COMMENT METHODS
    def test_post_commenting(self):
        self.post.comment(self.comment)
        self.assertIn(self.comment, self.post.get_comments())

    def test_post_invalid_commenting(self):
        comment = None
        self.assertRaises(self.post.comment(comment), "InvalidFunctionArguments")

    def test_post_deleting_comment(self):
        self.post.comment(self.comment)
        self.post.delete(self.comment)
        self.assertNotIn(self.comment, self.post.get_comments())
    
    def test_post_invalid_deleting_comment(self):
        comment = None
        self.assertRaises(self.post.delete(comment), "InvalidFunctionArguments")

    # TESTING USER-POST INTERACTION
    





        

    
        