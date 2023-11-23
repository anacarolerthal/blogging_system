from abc import ABC, abstractmethod
from typing import *
from content import Post
from model import BlogModel

class BaseUser(ABC):
    """Abstract class for a user"""
    def __init__(self, username: str, password: str, email: str, user_id: int = None):
        self.username = username
        self.password = password
        self.email = email
        self.id = user_id
    
    def set_user_id(self, user_id: int) -> None:
        self.id = user_id
    
    @abstractmethod
    def register(self, username: str, password: str, email: str) -> None:
        """Register a user"""
        pass
        
    def login(self, username: str, password: str) -> bool:
        """Login a user"""      
        pass

class User(BaseUser):
    """A user of the system
    
    username: str -> username of the user
    password: str -> password of the user
    email: str -> email of the user
    user_id: int -> id of the user
    """
    def __init__(self, username: str, password: str, email: str, posts: List[int] = None, 
                 followers: List[int] = None, following: List[int] = None, user_id: int = None):
        super().__init__(username, password, email, user_id)
        self.posts = posts if posts is not None else []
        self.followers = followers if followers is not None else []
        self.following = following if following is not None else []
    
    def post(self, post: Post) -> None:
        """Post a post"""
        pass   
        
    def like(self, post_id: int) -> None:
        """Like a post"""
        pass
    
    def follow(self, user_id: int) -> None:
        """Follow a user"""
        pass
    
class Moderator(BaseUser):
    """A moderator of the system
    
    username: str -> username of the moderator
    password: str -> password of the moderator
    email: str -> email of the moderator
    user_id: int -> id of the moderator
    """
    def __init__(self, username: str, password: str, email: str, user_id: int = None):
        super().__init__(username, password, email, user_id)
        
    def delete_post(self, post_id: int) -> None:
        """Delete a post"""
        pass
    
    def ban_user(self, user_id: int) -> None:
        """Ban a user"""
        pass
    
class UserFactory:
    """Factory class for users"""
    def create_user(self, user_type: str, username: str, password: str, email: str) -> User:
        """Create a user"""
        if user_type == 'user':
            return User(username, password, email)
        elif user_type == 'moderator':
            return Moderator(username, password, email)
        else:
            raise ValueError(f'User type {user_type} is not valid.')