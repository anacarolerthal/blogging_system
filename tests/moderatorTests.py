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
        self.moderator = Moderator(id = 2, username="moderator1", password="modpass", email="moderator1@example.com")
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
        with self.assertRaises(InvalidPostException) as context:
            self.moderator.delete_post(3)

        # assert
        self.assertEqual("O post não existe." , str(context.exception))

    def test_moderator_ban_user(self):
        user = User(username="user", password="pass", email="email@.com", id = 1,
                    posts = [], followers = [], following = [])

        # act
        self.moderator.ban_user(1)

        # assert 
        self.assertEqual(self.user.get_id(), 1)

    def test_moderator_ban_user_invalid_id(self):
        # act
        with self.assertRaises(InvalidUserException) as context:
            self.moderator.ban_user(2)

        # assert
        self.assertEqual("Usuário não existe." , str(context.exception))

    def test_moderator_ban_user_already_banned(self):
        # arrange
        user_2 = User(username="user", password="pass", email="email@.com", id = 2,
                    posts = [], followers = [], following = [])
        # act
        self.moderator.ban_user(2)
        with self.assertRaises(AlreadyBanned) as context:
            self.moderator.ban_user(2)

        # assert
        self.assertEqual("Usuário já banido." , str(context.exception))

    def test_moderator_unban_user(self):
        # arrange
        user_3 = User(username="user3", password="pass3", email="email3@.com", id = 3,
                    posts = [], followers = [], following = [])

        # act
        self.moderator.ban_user(3)
        self.moderator.unban_user(3)

        # assert
        self.assertEqual(user_3.get_id(), 3)

    def test_moderator_unban_user_invalid_id(self):
        # act
        with self.assertRaises(InvalidUserException) as context:
            self.moderator.unban_user(2)

        # assert
        self.assertEqual("Usuário não existe." , str(context.exception))

    def test_moderator_unban_user_already_unbanned(self):
        # arrange
        user_4 = User(username="user4", password="pass4", email="email4@.com", id = 4,
                    posts = [], followers = [], following = [])
        self.moderator.ban_user(4)
        self.moderator.unban_user(4)

        # act
        with self.assertRaises(AlreadyUnbanned) as context:
            self.moderator.unban_user(4)

        # assert
        self.assertEqual("Usuário já desbanido." , str(context.exception))






if __name__ == '__main__':
    unittest.main()
