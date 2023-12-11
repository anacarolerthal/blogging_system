from abc import ABC, abstractmethod
from model import BlogModel
from tags import Tag
from datetime import datetime
from typing import *

class BaseContent(ABC):
    """Abstract class for a content in the blog"""
    id: int
    author_id: int
    date: str
    content: str

    # REFACTORING
    # using BaseContent as a base class for Post and Reply, 
    # and defining the methods that are common to both classes here

    def get_id(self) -> int:
        return self.id

    def get_author_id(self) -> int:
        return self.author_id

    def get_date(self) -> str:
        return self.date

    def get_content(self) -> str:
        return self.content

    def set_id(self, id: int) -> None:
        if type(id) != int:
            raise TypeError("Tipo inválido de id. Ids devem ser inteiros.")
        self.id = id

    def set_date(self, date: str) -> None:
        if type(date) != str:
            raise TypeError("Tipo inválido para data. Ids devem ser Strings na forma 'YYYY-mm-dd hh:mm:ss'.")
        self.date = date

    # using abstract methods to force the implementation of these methods in the subclasses

    @abstractmethod
    def publish(self) -> None:
        """Publish a content"""

    def render(self) -> str:
        """Render a content on screen"""

class Post(BaseContent):
    """A post that is displayed in the feed"""
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
        return self.title

    def get_tags(self) -> List[str]:
        return self.tags

    def publish_tags(self) -> None:
        for tag in self.tags:
            tg = Tag(tag)
            tg.publish()
            tag_id = BlogModel().get_tag_id_by_name(tg.get_tag_name())
            BlogModel().create_tagged_post(self.id, tag_id)

    def publish(self):
        id = BlogModel().create_post(self)
        self.id = id
        self.publish_tags()

    def render(self) -> str:
        display = f"""
            -----{self.title}------- \n
            {self.content}
        """
        return display

class Reply(BaseContent):
    """A comment in a post"""
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
        return self.parent_post_id

    def publish(self) -> None:
        return BlogModel().create_reply(self)

    def render(self) -> str:
        display = f"""
        {self.content}
        """
        return display


