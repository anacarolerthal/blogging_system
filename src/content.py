from abc import ABC, abstractmethod
from model import BlogModel
from tags import Tag
from datetime import datetime
from typing import *

class BaseContent(ABC):
    """Abstract class for a content in the blog
    
    Attributes:
    id: int -> id of the content
    author_id: int -> id of the author of the content
    date: str -> date of the content
    content: str -> content of the post"""
    id: int
    author_id: int
    date: str
    content: str

    # REFACTORING
    # using BaseContent as a base class for Post and Reply, 
    # and defining the methods that are common to both classes here

    def get_id(self) -> int:
        """
        Get the id of the content

        Returns:
        self.id: int -> id of the content
        """
        return self.id

    def get_author_id(self) -> int:
        """
        Get the id of the author of the content

        Returns:
        self.author_id: int -> id of the author of the content
        """
        return self.author_id

    def get_date(self) -> str:
        """
        Get the date of the content

        Returns:
        self.date: str -> date of the content
        """
        return self.date

    def get_content(self) -> str:
        """
        Get the content of the content

        Returns:
        self.content: str -> content of the content
        """
        return self.content

    def set_id(self, id: int) -> None:
        """
        Set the id of the content

        Args:
        id: int -> id of the content

        Raises:
        TypeError -> if the type of id is not int
        """
        if type(id) != int:
            raise TypeError("Tipo inválido de id. Ids devem ser inteiros.")
        self.id = id

    def set_date(self, date: str) -> None:
        """
        Set the date of the content

        Args:
        date: str -> date of the content

        Raises:
        TypeError -> if the type of date is not str
        """
        if type(date) != str:
            raise TypeError("Tipo inválido para data. Ids devem ser Strings na forma 'YYYY-mm-dd hh:mm:ss'.")
        self.date = date

    # using abstract methods to force the implementation of these methods in the subclasses

    @abstractmethod
    def publish(self) -> None:
        """ Abstract method to publish a content on the blog """

    def render(self) -> str:
        """ Abstract method to render a content on the blog """

class Post(BaseContent):
    """A post that is displayed in the feed

    Attributes:
    id: int -> id of the post
    author_id: int -> id of the author of the post
    date: str -> date of the post
    title: str -> title of the post
    content: str -> content of the post
    tags: List[str] -> list of tags of the post
    """
    def __init__(self,
                 author_id: int,
                 title: str,
                 id: int = None,
                 date: str = None,
                 content: str = None,
                 tags: List[str] = None):
        self.id = id
        self.author_id = author_id
        self.date = date
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    # OLD VERSION
    # def get_id(self) -> int:
    #     return self.id

    # def get_author_id(self) -> int:
    #     return self.author_id

    # def get_date(self) -> str:
    #     return self.date

    # def get_content(self) -> str:
    #     return self.content

    def get_title(self) -> str:
        """
        Get the title of the post

        Returns:
        self.title: str -> title of the post
        """
        return self.title

    def get_tags(self) -> List[str]:
        """
        Get the tags of the post

        Returns:
        self.tags: List[str] -> list of tags of the post
        """
        return self.tags

    def publish_tags(self) -> None:
        """
        Publish the tags of the post

        Raises:
        TypeError -> if the type of tag is not str
        """
        for tag in self.tags:
            tg = Tag(tag)
            tg.publish()
            tag_id = BlogModel().get_tag_id_by_name(tg.get_tag_name())
            BlogModel().create_tagged_post(self.id, tag_id)

    def publish(self):
        """Publish the post"""
        id = BlogModel().create_post(self)
        self.id = id
        self.publish_tags()

    def render(self) -> str:
        """Render the post"""
        display = f"""
            -----{self.title}------- \n
            {self.content}
        """
        return display

class Reply(BaseContent):
    """A reply in a post

    Attributes:
    id: int -> id of the reply
    author_id: int -> id of the author of the reply
    date: str -> date of the reply
    parent_post_id: int -> id of the parent post of the reply
    content: str -> content of the reply
    """
    def __init__(self,
                 author_id: int,
                 parent_post_id: int,
                 id: int = None,
                 date: str = None,
                 content: str = None,
                 tags: List[str] = None):
        self.id = None
        self.author_id = author_id
        self.date = date
        self.parent_post_id = parent_post_id
        self.content = content

    def get_parent_post(self) -> int:
        """
        Get the parent post of the reply

        Returns:
        self.parent_post_id: int -> id of the parent post of the reply
        """
        return self.parent_post_id

    def publish(self) -> None:
        """Publish the reply"""
        return BlogModel().create_reply(self)

    def render(self) -> str:
        """Render the reply"""
        display = f"""
        {self.content}
        """
        return display


