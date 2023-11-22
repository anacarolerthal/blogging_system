from abc import ABC, abstractmethod

class Post(ABC):
    """Abstract class for a post"""
    def set_post_id(self, post_id: int) -> None:
        """Set the post id

        Args:
            post_id (int): The post id retrieved from the database
        """
        self.id = post_id

    def set_post_date(self, date: str) -> None:
        """Set the post date

        Args:
            date (str): The date the post was created retrieved from the database. Format: DD-MM-YYYY
        """
        self.date = date


class FeedPost(Post):
    """A post that is displayed in the feed"""
    def __init__(self, title: str, content: str, author_id: int, post_id: int = None, comments: list = [], date: str = None) -> None:
        """Initialize the feed post

        Args:
            title (str): The title of the post
            content (str): The content of the post
            author_id (int): The id of the user that created the post
            post_id (int, optional): The id of the post retrieved from the database. When creating a new post, this is None. Defaults to None.
            comments (list, optional): A list of ids of comments on the post. Defaults to [].
            date (str, optional): The date the post was created retrieved from the database. Format: DD-MM-YYYY. Defaults to None.
        """
        self.title = title
        self.content = content
        self.author_id = author_id
        self.id = post_id
        self.comments = comments
        self.date = date

class CommentPost(Post):
    """A comment in a post"""
    def __init__(self, content: str, author_id: int, parent_post: int, post_id: int = None, date: str = None) -> None:
        """Initialize the comment post

        Args:
            content (str): The content of the comment
            author_id (int): The id of the user that created the comment
            parent_post (int): The id of the post that the comment is on
            post_id (int, optional): The id of the post retrieved from the database. When creating a new post, this is None. Defaults to None.
            date (str, optional): The date the post was created retrieved from the database. Format: DD-MM-YYYY. Defaults to None.
        """
        self.content = content
        self.author_id = author_id
        self.parent_post = parent_post
        self.id = post_id
        self.date = date

class PostFactory(ABC):
    """Factory class for posts"""
    @abstractmethod
    def create_post():
        """Create a post"""
        pass

class FeedPostFactory(PostFactory):
    """Factory class for feed posts"""
    def create_post(self, title: str, content: str, author_id: int, post_id: int = None, comments: list = [], date: str = None) -> FeedPost:
        """Create a feed post

        Args:
            title (str): The title of the post
            content (str): The content of the post
            author_id (int): The id of the user that created the post
            post_id (int, optional): The id of the post retrieved from the database. When creating a new post, this is None. Defaults to None.
            comments (list, optional): A list of ids of comments on the post. Defaults to [].
            date (str, optional): The date the post was created retrieved from the database. Format: DD-MM-YYYY. Defaults to None.

        Returns:
            FeedPost: The feed post
        """
        return FeedPost(title, content, author_id, post_id, comments, date)

class CommentPostFactory(PostFactory):
    """Factory class for comment posts"""
    def create_post(self, content: str, author_id: int, parent_post: int, post_id: int = None, date: str = None) -> CommentPost:
        """Create a comment post

        Args:
            content (str): The content of the comment
            author_id (int): The id of the user that created the comment
            parent_post (int): The id of the post that the comment is on
            post_id (int, optional): The id of the post retrieved from the database. When creating a new post, this is None. Defaults to None.
            date (str, optional): The date the post was created retrieved from the database. Format: DD-MM-YYYY. Defaults to None.

        Returns:
            CommentPost: The comment post
        """
        return CommentPost(content, author_id, parent_post, post_id, date)











