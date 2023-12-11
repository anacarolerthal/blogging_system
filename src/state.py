from abc import ABC, abstractmethod

class UserLoginState(ABC):
    @abstractmethod
    def is_logged_in(self) -> bool:
        pass

class LoggedInState(UserLoginState):
    def is_logged_in(self) -> bool:
        return True

class LoggedOutState(UserLoginState):
    def is_logged_in(self) -> bool:
        return False