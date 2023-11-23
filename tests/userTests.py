"""Creating Tests for the User Class in TDD format"""
import unittest
import sys

sys.path.append('../')
from src.users import User, Moderator, UserFactory
from src.content import Post

#User creation
class TestUserSystem(unittest.TestCase):
    def setUp(self):
        # Initialize objects for testing
        self.user = User(username="user1", password="pass1", email="user1@example.com")
        self.moderator = Moderator(username="moderator1", password="modpass", email="moderator1@example.com")
        self.user_factory = UserFactory()

    # TESTING GETTERS
    def test_user_get_posts(self):
        self.assertIsInstance(self.user.get_posts(), list)

    def test_user_get_following(self):
        self.assertIsInstance(self.user.get_following(), list)

    def test_user_get_followers(self):
        self.assertIsInstance(self.user.get_followers(), list)

    def test_user_get_username(self):
        self.assertIsInstance(self.user.get_username(), str)

    def test_user_get_email(self):
        self.assertIsInstance(self.user.get_email(), str)

    def test_user_get_id(self):
        self.assertIsInstance(self.user.get_id(), int)

    def test_user_get_type(self):
        self.assertIsInstance(self.user.get_type(), str)

    # TESTING POST INTERACTIONS

    def test_user_posting(self):
        post = Post(content="This is a test post.")
        self.user.post(post)
        self.assertIn(post, self.user.get_posts())

    def test_user_invalid_posting(self):
        post = None
        #Assert if error "InvalidPost" is raised
        self.assertRaises(self.user.post(post), "InvalidFunctionArguments")

    def test_user_deleting(self):
        postId = 1
        authorId = self.user.get_id()
        post = Post(id=postId, title="Title",  content="This is a test post.", author_id=authorId)
        self.user.post(post)
        self.user.delete(postId)
        self.assertNotIn(post, self.user.get_posts())

    def test_user_deleting_others_post(self):
        postId = 1
        authorId = self.user.get_id() + 1
        post = Post(id=postId, title="Title",  content="This is a test post.", author_id=authorId)
        self.user.post(post)
        self.assertRaises(self.user.delete(postId), "PermissionFailed")

    def test_user_invalid_deleting(self):
        post = None
        #Assert if error "InvalidPost" is raised
        self.assertRaises(self.user.delete(post), "InvalidPost")

    # TESTING USER-USER INTERACTION

    def test_user_follow(self):
        other_user_id = 2
        self.user.follow(other_user_id)
        self.assertIn(other_user_id, self.user.get_all_following())

    def test_user_unfollow(self):
        other_user_id = 2
        self.user.unfollow(other_user_id)
        self.assertNotIn(other_user_id, self.user.get_all_following())

    def test_user_follow_self(self):
        self.user.follow(self.user.get_id())
        #Assert if error "CannotFollowSelf" is raised
        self.assertRaises(self.user.follow(self.user.get_id()), "CannotFollowSelf")

    def test_user_unfollow_self(self):
        self.user.unfollow(self.user.get_id())
        #Assert if error "CannotUnfollowSelf" is raised
        self.assertRaises(self.user.follow(self.user.get_id()), "CannotUnfollowSelf")     

    def test_user_follow_already_following(self):
        other_user_id = 2
        self.user.follow(other_user_id)
        #Assert if error "AlreadyFollowing" is raised
        self.assertRaises(self.user.follow(other_user_id), "AlreadyFollowing")

    def test_user_unfollow_already_unfollowing(self):
        other_user_id = 2
        self.user.unfollow(other_user_id)
        #Assert if error "AlreadyUnfollowing" is raised
        self.assertRaises(self.user.unfollow(other_user_id), "AlreadyUnfollowing")

    def test_user_follow_invalid_user(self):
        other_user_id = 100
        #Assert if error "InvalidUser" is raised
        self.assertRaises(self.user.follow(other_user_id), "UserNotInDatabase")

    def test_user_unfollow_invalid_user(self):
        other_user_id = 100
        #Assert if error "InvalidUser" is raised
        self.assertRaises(self.user.unfollow(other_user_id), "UserNotInDatabase")

    def test_user_follow_invalid_entry(self):
        # assert if User type is not int
        other_user_id = None
        self.assertRaises(self.user.follow(other_user_id), "InvalidFunctionArguments")

    def test_user_unfollow_invalid_entry(self):
        # assert if User type is not int
        other_user_id = None
        self.assertRaises(self.user.unfollow(other_user_id), "InvalidFunctionArguments")

    # TESTING MODERATOR INTERACTION

    def test_moderator_delete_post(self):
        postId = 1
        authorId = self.user.get_id()
        post = Post(id=postId, title="Title",  content="This is a test post.", author_id=authorId)
        self.moderator.delete_post(post)
        self.assertNotIn(post, self.user.get_posts())

    def test_moderator_delete_post_invalid_post(self):
        post = None
        #Assert if error "InvalidPost" is raised
        self.assertRaises(self.moderator.delete_post(post), "InvalidPost")

    def test_moderator_ban_user(self):
        userId = 1
        self.moderator.ban_user(userId)
        self.assertIn(userId, self.moderator.get_banned_users())

    def test_moderator_ban_user_invalid_user(self):
        userId = 100
        #Assert if error "InvalidUser" is raised
        self.assertRaises(self.moderator.ban_user(userId), "UserNotInDatabase")

    def test_moderator_unban_user(self):
        userId = 1
        self.moderator.unban_user(userId)
        self.assertNotIn(userId, self.moderator.get_banned_users())

    def test_moderator_unban_user_invalid_user(self):
        userId = 100
        #Assert if error "InvalidUser" is raised
        self.assertRaises(self.moderator.unban_user(userId), "UserNotInDatabase")

    def test_moderator_unban_user_not_banned(self):
        userId = 1
        #Assert if error "UserNotBanned" is raised
        self.assertRaises(self.moderator.unban_user(userId), "UserNotBanned")

    def test_moderator_ban_user_already_banned(self):
        userId = 1
        self.moderator.ban_user(userId)
        #Assert if error "UserAlreadyBanned" is raised
        self.assertRaises(self.moderator.ban_user(userId), "UserAlreadyBanned")

    def test_moderator_ban_other_moderator(self):
        userId = 2
        #Assert if error "CannotBanModerator" is raised
        self.assertRaises(self.moderator.ban_user(userId), "CannotBanModerator")



    def test_user_factory_create_user(self):
        created_user = self.user_factory.create_user("user", "user2", "pass2", "user2@example.com")
        self.assertIsInstance(created_user, User)

        created_moderator = self.user_factory.create_user("moderator", "moderator2", "modpass2", "moderator2@example.com")
        self.assertIsInstance(created_moderator, Moderator)

        with self.assertRaises(ValueError):
            self.user_factory.create_user("invalid_type", "invalid", "pass", "invalid@example.com")

if __name__ == '__main__':
    unittest.main()
