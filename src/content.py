from abc import ABC, abstractmethod
from model import BlogModel
from datetime import datetime

class BaseContent(ABC):
    """Abstract class for a content in the blog"""
    id: int
    author_id: int
    date: str
    content: str
    image: str

    @abstractmethod
    def publish(self):
        """Publish a content"""

    def delete(self):
        """Delete a content on database"""

    def render(self):
        """Render a content on screen"""

class Post(BaseContent):
    """A post that is displayed in the feed"""
    def __init__(self,
                 author_id,
                 date,
                 title,
                 content = None,
                 image = None):
        self.id = None,
        self.author_id = author_id,
        self.date = date
        self.title = title,
        self.content = content,
        self.image = image

    def publish(self):
        return BlogModel.create_post(self)
    
    def delete(self):
        return super().delete()
    
    def render(self):
        return super().render()
        
class Comment(BaseContent):
    """A comment in a post"""
    def __init__(self,
                 author_id,
                 date,
                 parent_post_id,
                 content = None,
                 image = None):
        self.id = None,
        self.author_id = author_id,
        self.date = date,
        self.parent_post_id = parent_post_id
        self.content = content,
        self.image = image

    def publish(self):
        return BlogModel.create_comment(self)
    
    def delete(self):
        return super().delete()
    
    def render(self):
        return super().render()
    
#Simple Factory
class ContentFactory:
    @staticmethod
    def get_content(type_: str) -> BaseContent:
        if type_ == "POST":
            return Post()
        if type_ == "COMMENT":
            return Comment()
        else:
            raise ValueError(f"Content type {type_} not found")











