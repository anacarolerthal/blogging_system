from abc import ABC, abstractmethod
from typing import *

from src.content import Post
#from model import BlogModel


class BaseUser(ABC):
    """Abstract class for a user

    username: str -> username of the user
    password: str -> password of the user
    email: str -> email of the user
    user_id: int -> id of the user
    """

    id: int
    username: str
    password: str
    email: str

    # def set_user_id(self, user_id: int) -> None:
    #     self.id = user_id

    # @abstractmethod
    # def register(self, username: str, password: str, email: str) -> None:
    #     """Register a user"""
    #     pass

    # @abstractmethod
    # def login(self, username: str, password: str) -> bool:
    #     """Login a user"""      
    #     pass

class User(BaseUser):
    """A user of the system
    """
    def __init__(self,
                 username: str,
                 password: str,
                 email: str,
                 id: int = None,
                 posts: List[int] = None, 
                 followers: List[int] = None,
                 following: List[int] = None):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__email = email
        self.__posts = posts if posts is not None else []
        self.__followers = followers if followers is not None else []
        self.__following = following if following is not None else []

    def get_id(self) -> int:
        """Get the id of the user"""
        return self.__id

    def get_username(self) -> str:
        """Get the username of the user"""
        return self.__username

    def get_email(self) -> str:
        """Get the email of the user"""
        return self.__email

    def get_posts(self) -> List[int]:
        """Get the posts of the user"""
        return self.__posts

    def get_followers(self) -> List[int]:
        """Get the followers of the user"""
        return self.__followers

    def get_following(self) -> List[int]:
        """Get the following of the user"""
        return self.__following


    def post(self, post: Post) -> None:
        """Post a post"""
        pass  

    def delete_post(self, post_id: int) -> None:
        """Delete a post"""
        pass

    def like(self, post_id: int) -> None:
        """Like a post"""
        pass

    def follow(self, user_id: int) -> None:
        """Follow a user"""
        pass

class Moderator(BaseUser):
    """A moderator of the system"""
    def __init__(self, 
                 username: str,
                 password: str,
                 email: str,
                 id: int = None):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__email = email

    def get_id(self) -> int:
        """Get the id of the user"""
        return self.__id

    def get_username(self) -> str:
        """Get the username of the user"""
        return self.__username

    def get_email(self) -> str:
        """Get the email of the user"""
        return self.__email

    def delete_post(self, post_id: int) -> None:
        """Delete a post"""
        pass

    def ban_user(self, user_id: int) -> None:
        """Ban a user"""
        pass
      
    def unban_user(self, user_id: int) -> None:
        """Unban a user"""
        pass

class UserFactory:
    """Factory class for users"""
    @staticmethod
    def create_user(type_: str) -> User:
        """Create a user"""
        if type_ == 'USER':
            return User()
        elif type_ == 'MODERATOR':
            return Moderator()
        else:
            raise ValueError(f'User type {type_} is not valid.')
            