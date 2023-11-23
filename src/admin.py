import model
blog_model = model.BlogModel()

class Admin:
    def authenticate(self, username: str, password: str):
        """Authenticate a user
        
        username: str -> username of the user
        password: str -> password of the user
        """
        return blog_model.check_user(username, password)
    
    def register(self, username: str, password: str, email: str):
        """Register a user
        
        username: str -> username of the user
        password: str -> password of the user
        email: str -> email of the user
        """
        blog_model.add_user(username, password, email)