from abc import ABC, abstractmethod

class BaseUser(ABC):
    """Abstract class for a user"""

class User(BaseUser):
    """A user of the system"""
    
class Moderator(BaseUser):
    """A moderator of the system"""
    
class UserFactory:
    """Factory class for users"""