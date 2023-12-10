import unittest
import sys

#APPENDS SRC FOLDER TO PATH
sys.path.append('./src')

from users import User, Moderator
from content import Post, Reply
from tags import Tag

class TestTagSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.tag = Tag(tag_name="tag1", tag_id=1)

    def test_tag_get_id(self):
        # act
        id = self.tag.get_tag_id()
        # assert
        self.assertIsInstance(id, int)

    def test_tag_get_name(self):
        # act
        name = self.tag.get_tag_name()
        # assert
        self.assertIsInstance(name, str)

    def test_tag_set_id(self):

        # act
        self.tag.set_tag_id(2)
        # assert
        self.assertEqual(self.tag.get_tag_id(), 2)

    def test_tag_publish(self):
        # act
        self.tag.publish()
        # assert
        self.assertEqual(self.tag.get_tag_id(), 1)

    def test_tag_publish_already_in_db(self):
        # act
        self.tag.publish()
        # assert
        self.assertEqual(self.tag.get_tag_id(), 1)

if __name__ == '__main__':
    unittest.main()
