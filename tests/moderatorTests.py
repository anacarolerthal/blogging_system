"""Creating Tests for the User Class in TDD format"""
import unittest
import sys

#APPENDS SRC FOLDER TO PATH
sys.path.append('./src')

from users import User, Moderator, UserFactory
from content import Post
from customExceptions import *

# moderator creation
class TestModeratorSystem(unittest.TestCase):
    def setUp(self):
        # arrange
        # Initialize objects for testing
        self.user = User(username="user1", password="pass1", email="email1@.com", id = 1,
                         posts = [1, 2], followers = [], following = [])
        self.moderator = Moderator(username="moderator1", password="modpass", email="moderator1@example.com")
        self.user_factory = UserFactory()

    # TESTING GETTERS
    def test_moderator_get_id(self):
        # act
        id = self.moderator.get_id()

        # assert
        self.assertIsInstance(id, int)

    def test_moderator_get_username(self):
        # act
        username = self.moderator.get_username()

        # assert
        self.assertIsInstance(username, str)

    def test_moderator_get_email(self):
        # act
        email = self.moderator.get_email()

        # assert
        self.assertIsInstance(email, str)

    def test_moderator_set_id(self):
        # act
        self.moderator.set_id(2)
        id = self.moderator.get_id()

        # assert
        self.assertEqual(id, 2)

    def test_moderator_set_invalid_id(self):
        # act
        moderator_id = None
        with self.assertRaises(TypeError) as context:
            self.user.set_id(moderator_id)

        # assert
        self.assertEqual("Tipo inválido de id. Ids devem ser inteiros." , str(context.exception))


    # TESTING MODERATOR USER INTERACTION
    def test_moderator_delete_post(self):
        # act
        self.moderator.delete_post(1)

        # assert
        self.assertEqual(self.user.get_posts(), [2])

    def test_moderator_delete_post_invalid_id(self):
        # act
        with self.assertRaises(InvalidPostId) as context:
            self.moderator.delete_post(3)

        # assert
        self.assertEqual("Post não existe." , str(context.exception))

    def test_moderator_ban_user(self):
        # act
        self.moderator.ban_user(1)

        # assert
        self.assertEqual(self.user.get_id(), 1)

    def test_moderator_ban_user_invalid_id(self):
        # act
        with self.assertRaises(InvalidUserId) as context:
            self.moderator.ban_user(2)

        # assert
        self.assertEqual("Usuário não existe." , str(context.exception))

    def test_moderator_unban_user(self):
        # act
        self.moderator.unban_user(1)

        # assert
        self.assertEqual(self.user.get_id(), 1)

    def test_moderator_unban_user_invalid_id(self):
        # act
        with self.assertRaises(InvalidUserId) as context:
            self.moderator.unban_user(2)

        # assert
        self.assertEqual("Usuário não existe." , str(context.exception))





if __name__ == '__main__':
    unittest.main()
