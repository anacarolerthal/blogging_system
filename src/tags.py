from abc import ABC, abstractmethod
from model import BlogModel

class Tag():
    def __init__(self,
                tag_name: str,
                tag_id: int = None):

        self.tag_id = tag_id 
        self.tag_name = tag_name

    def get_tag_id(self) -> int:
        return self.tag_id

    def get_tag_name(self) -> str:
        return self.tag_name
    
    def set_tag_id(self, tag_id) -> None:
        self.tag_id = tag_id
        pass
    
    def publish(self) -> None:
        if not BlogModel().check_if_tag_in_db(self.tag_name):
            id_tag = BlogModel().create_tag(self.tag_name)
            self.tag_id = id_tag
        pass