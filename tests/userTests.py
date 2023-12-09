"""Creating Tests for the User Class in TDD format"""
import unittest
import sys

#APPENDS SRC FOLDER TO PATH
sys.path.append('../')
sys.path.append('../src')

from src.users import User, Moderator, UserFactory
from src.content import Post

#User creation
class TestUserSystem(unittest.TestCase):
    def setUp(self):
        # arrange
        # Initialize objects for testing
        self.user = User(username="user1", password="pass1", email="email@email.com", id = 1,
                         posts = [], followers = [], following = [])
        self.moderator = Moderator(username="moderator1", password="modpass", email="moderator1@example.com")
        self.user_factory = UserFactory()

    # TESTING GETTERS
    def test_user_get_id(self):
        # act
        id = self.user.get_id()
        # assert
        self.assertIsInstance(id, int)

    def test_user_get_username(self):
        # act
        username = self.user.get_username()
        # assert
        self.assertIsInstance(username, str)

    def test_user_get_email(self):
        # act
        email = self.user.get_email()
        # assert
        self.assertIsInstance(email, str)

    def test_user_get_posts(self):
        # act
        posts = self.user.get_posts()
        # assert
        self.assertIsInstance(posts, list)

    def test_user_get_followers(self):
        # act
        followers = self.user.get_followers()
        # assert
        self.assertIsInstance(followers, list)

    def test_user_get_following(self):
        # act
        following = self.user.get_following()
        # assert
        self.assertIsInstance(following, list)

    # TESTING SETTERS
    def test_user_set_id(self):
        # act
        self.user.set_id(2)
        # assert
        self.assertEqual(self.user.get_id(), 2)

    def test_user_set_invalid_id(self):
        # arrange
        user_Id = None

        # act
        with self.assertRaises(TypeError) as context:
            self.user.set_id(user_Id)

        # assert
        self.assertEqual("Tipo inválido de id. Ids devem ser inteiros." , str(context.exception))

    # TESTING USER-USER INTERACTION

    def test_user_follow(self):
        # arrange
        other_user_id = 2

        # act
        self.user.follow(other_user_id)
        
        # assert
        self.assertIn(other_user_id, self.user.get_following())

    def test_user_unfollow(self):
        # arrange
        other_user_id = 2

        # act
        self.user.unfollow(other_user_id)

        # assert
        self.assertNotIn(other_user_id, self.user.get_following())

    def test_user_follow_self(self):
        # arrange
        id_self = self.user.get_id()

        # act
        with self.assertRaises(self.user.follow(self.user.get_id()), "CannotFollowSelf") as context:
            self.user.follow(id_self)

        # assert
        self.assertEqual("Não é possível seguir a si mesmo." , str(context.exception))

    def test_user_unfollow_self(self):
        # arrange
        id_self = self.user.get_id()

        # act
        with self.assertRaises(self.user.unfollow(self.user.get_id()), "CannotUnfollowSelf") as context:
            self.user.unfollow(id_self)

        # assert
        self.assertEqual("Não é possível deixar de seguir a si mesmo." , str(context.exception))

    def test_user_follow_already_following(self):
        # arrange
        other_user_id = 2
        self.user.follow(other_user_id)

        # act
        with self.assertRaises(self.user.follow(other_user_id), "AlreadyFollowing") as context:
            self.user.follow(other_user_id)

        # assert
        self.assertEqual("Não é possível seguir novamente o mesmo usuário." , str(context.exception))

    def test_user_unfollow_already_not_following(self):
        # arrange
        other_user_id = 2
        self.user.unfollow(other_user_id)

        # act
        with self.assertRaises(self.user.unfollow(other_user_id), "AlreadyNotFollowing") as context:
            self.user.unfollow(other_user_id)

        # assert
        self.assertEqual("Não é possível deixar de seguir novamente o mesmo usuário.",  str(context.exception))

    def test_user_follow_invalid_user(self):
        # arrange
        other_user_id = 100

        # act
        with self.assertRaises(self.user.follow(other_user_id), "AlreadyNotFollowing") as context:
            self.user.follow(other_user_id)

        # assert
        self.assertEqual("Não é possível deixar de seguir novamente o mesmo usuário.",  str(context.exception))


    def test_user_unfollow_invalid_user(self):
        # arrange
        other_user_id = 100

        # act
        with self.assertRaises(self.user.unfollow(other_user_id), "AlreadyNotFollowing") as context:
            self.user.unfollow(other_user_id)

        # assert
        self.assertRaises(self.user.unfollow(other_user_id), "UserNotInDatabase")


if __name__ == '__main__':
    unittest.main()
