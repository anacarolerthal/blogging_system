from abc import ABC, abstractmethod
from typing import *

class Post(ABC):
    """Abstract class for a post
    
    content: str -> content of the post
    post_id: int -> id of the post
    author: str -> author of the post
    date: str -> date of the post    
    """
    @abstractmethod
    def set_post_id(self, post_id: int = None) -> None:
        pass
    
class FeedPost(Post):
    """A post that is displayed in the feed
    
    title: str -> title of the post
    comments: List[str] -> comments of the post if any
    tags: List[str] -> tags of the post (at least one)
    content: str -> content of the post
    post_id: int -> id of the post
    author: str -> author of the post
    date: str -> date of the post
    """
    def __init__(self, title: str, tags: List[str] , content: str, author: str, comments: List[str] = None, date: str = None, post_id: int = None):
        super().__init__(content, post_id, author, date)
        self.title = title
        self.tags = tags
        self.comments = comments if comments else []
        self.content = content
        self.id = post_id
        self.author = author
        self.date = date


    def set_post_id(self, post_id: int) -> None:
        self.id = post_id

class CommentPost(Post):
    """A comment in a post
    
    parent_post: Post -> parent post of the comment (Post object)
    content: str -> content of the comment
    post_id: int -> id of the comment
    author: str -> author of the comment
    date: str -> date of the comment
    """
    def __init__(self, parent_post: Post, content: str, author: str, date: str = None, post_id: int = None):
        super().__init__(content, post_id, author, date)
        self.parent_post = parent_post
        self.content = content
        self.id = post_id
        self.author = author
        self.date = date


    def set_post_id(self, post_id: int) -> None:
        self.id = post_id

class PostFactory:
    """Factory class for posts"""
    @staticmethod
    def create_post(post_type: str, content: str, author:str, title: str = None, tags:List[str] = None, comments: List[str] = None, parent_post: Post = None, post_id: int = None, date:str = None) -> Post:
        """Create a post
        
        post_type: str -> type of the post (feed or comment)
        content: str -> content of the post
        author: str -> author of the post
        title: str -> title of the post
        tags: List[str] -> tags of the post if any
        comments: List[str] -> comments of the post if any
        parent_post: Post -> parent post of the comment if any
        post_id: int -> id of the post
        date: str -> date of the post
        """

        if post_type == 'feed':
            return FeedPost(title, tags, content, author, comments, date, post_id)
        elif post_type == 'comment':
            return CommentPost(parent_post, content, author, date, post_id)
        else:
            raise ValueError(f'Post type {post_type} is not valid.')
