import model

class Admin:
    model = model.BlogModel()

    def authenticate(username: str, password: str):
        """Authenticate a user
        
        username: str -> username of the user
        password: str -> password of the user
        """
        return model.check_user(username, password)
    
    def register(username: str, password: str, email: str):
        """Register a user
        
        username: str -> username of the user
        password: str -> password of the user
        email: str -> email of the user
        """
        model.add_user(username, password, email)