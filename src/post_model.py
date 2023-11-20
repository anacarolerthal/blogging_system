from abc import ABC, abstractmethod

class Post(ABC):
    """Abstract class for a post"""
    def set_post_id(self, post_id):
        self.id = post_id


class FeedPost(Post):
    """A post that is displayed in the feed"""
    def __init__(self, title, content, author, post_id=None, comments=[], date=None):
        self.title = title
        self.content = content
        self.author = author
        self.id = post_id
        self.comments = comments
        self.date = date

class CommentPost(Post):
    """A comment in a post"""
    def __init__(self, title, content, parent_post, post_id=None):
        self.title = title
        self.content = content
        self.parent_post = parent_post
        self.id = post_id




class PostFactory:
    """Factory class for posts"""
    def create_post(self, post_type, title, content, parent_post=None):
        """Create a post"""
        if post_type == 'feed':
            return FeedPost(title, content)
        elif post_type == 'comment':
            return CommentPost(title, content, parent_post)
        else:
            raise ValueError(f'Post type {post_type} is not valid.')
















