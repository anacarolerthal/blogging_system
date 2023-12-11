from abc import ABC, abstractmethod
from model import BlogModel

class Tag():
    """Class for a tag

    Attributes:
    tag_id: int -> id of the tag
    tag_name: str -> name of the tag
    """
    def __init__(self,
                tag_name: str,
                tag_id: int = None):

        self.tag_id = tag_id
        self.tag_name = tag_name

    def get_tag_id(self) -> int:
        """
        Get the id of the tag

        Returns:
        self.tag_id: int -> id of the tag
        """
        return self.tag_id

    def get_tag_name(self) -> str:
        """
        Get the name of the tag

        Returns:
        self.tag_name: str -> name of the tag
        """
        return self.tag_name

    def set_tag_id(self, tag_id) -> None:
        """
        Set the id of the tag

        Args:
        tag_id: int -> id of the tag

        Raises:
        TypeError -> if the type of id is not int
        """
        self.tag_id = tag_id

    def publish(self) -> None:
        """
        Publish the tag

        Raises:
        TypeError -> if the type of tag is not str
        """
        if not BlogModel().check_if_tag_in_db(self.tag_name):
            id_tag = BlogModel().create_tag(self.tag_name)
            self.tag_id = id_tag