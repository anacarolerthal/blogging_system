from abc import ABC, abstractmethod
from typing import *

class Post(ABC):
    """Abstract class for a post"""
    @abstractmethod
    def set_post_id(self, post_id: int) -> None:
        pass

class FeedPost(Post):
    # envoltorio em um padrão decorator
    """A post that is displayed in the feed"""
    def __init__(self, title: str, content: str, author: str, post_id: int = None, comments: List[str] = None, date: str = None):
        self.title = title
        self.content = content
        self.author = author
        self.id = post_id
        self.comments = comments if comments else []
        self.date = date

    # talvez nao seja necessario um metodo abstrato
    def set_post_id(self, post_id: int) -> None:
        self.id = post_id

class CommentPost(Post):
    # decorator em um padrão decorator
    """A comment in a post"""
    def __init__(self, title: str, content: str, parent_post: Post, post_id: int = None):
        self.title = title
        self.content = content
        self.parent_post = parent_post
        self.id = post_id

    def set_post_id(self, post_id: int) -> None:
        self.id = post_id

class PostFactory:
    """Factory class for posts"""
    @staticmethod
    def create_post(post_type: str, title: str, content: str, parent_post: Post = None) -> Post:
        """Create a post"""
        if post_type == 'feed':
            return FeedPost(title, content)
        elif post_type == 'comment':
            return CommentPost(title, content, parent_post)
        else:
            raise ValueError(f'Post type {post_type} is not valid.')
