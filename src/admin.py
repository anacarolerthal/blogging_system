import model

user_model = model.BlogModel()

class Admin:
    def authenticate(self, username: str, password: str):
        """Authenticate a user
        
        username: str -> username of the user
        password: str -> password of the user
        """
        return user_model.check_user(username, password)
    
    def is_moderator(self, username: str):
        """Check if a user is a moderator
        
        username: str -> username of the user
        """
        return user_model.check_if_moderator(username)

    def register(self, username: str, password: str, email: str, is_moderator: bool = False):
        """Register a user

        username: str -> username of the user
        password: str -> password of the user
        email: str -> email of the user
        """
        user_model.add_user(username, password, email, is_moderator)

    def getId(self, username: str):
        """
        Get id from a username
        """
        return user_model.get_user_id_by_username(username)
