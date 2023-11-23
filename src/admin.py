import model

user_model = model.BlogModel()

class Admin:
    def authenticate(self, username: str, password: str):
        """Authenticate a user
        
        username: str -> username of the user
        password: str -> password of the user
        """
        return user_model.check_user(username, password)
    
    def register(self, username: str, password: str, email: str):
        """Register a user
        
        username: str -> username of the user
        password: str -> password of the user
        email: str -> email of the user
        """
        user_model.add_user(username, password, email)
