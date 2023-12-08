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
    def publish(self) -> None:
        """Publish a content"""

    def delete(self) -> None:
        """Delete a content on database"""

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
                 image: str = None):
        self.id = id
        self.author_id = author_id
        self.date = date
        self.title = title
        self.content = content
        self.image = image

    def get_id(self) -> int:
        return self.id

    def get_author_id(self) -> int:
        return self.author_id

    def get_date(self) -> str:
        return self.date

    def get_title(self) -> str:
        return self.title

    def get_content(self) -> str:
        return self.content

    def get_image(self) -> str:
        return self.image

    def set_id(self, id: int) -> None:
        if type(id) != int:
            raise TypeError("Tipo inválido de id. Ids devem ser inteiros.")
        self.id = id

    def set_date(self, date: str) -> None:
        if type(date) != str:
            raise TypeError("Tipo inválido para data. Ids devem ser Strings na forma 'YYYY-mm-dd hh:mm:ss'.")
        self.date = date

    def publish(self):
        id = BlogModel().create_post(self)
        return id
    
    def delete(self) -> None:
        return super().delete()
    
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
                 image: str = None):
        self.id = None
        self.author_id = author_id
        self.date = date
        self.parent_post_id = parent_post_id
        self.content = content
        self.image = image

    def publish(self) -> None:
        return BlogModel().create_reply(self)
    
    def delete(self) -> None:
        return super().delete()
    
    def render(self) -> str:
        display = f"""
        {self.content}
        """
        return display
    
#Simple Factory
# class ContentFactory:
#     @staticmethod
#     def get_content(type_: str, args) -> BaseContent:
#         if type_ == "POST":
#             return Post(args.author_id,
#                         args.title,
#                         args.content,
#                         args.image,
#                         )
#         if type_ == "REPLY":
#             return Reply(args)
#         else:
#             raise ValueError(f"Content type {type_} not found")


