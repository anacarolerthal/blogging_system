import model

model = model.BlogModel()


def authenticate(username, password):
    """Authenticate a user
    
    username: str -> username of the user
    password: str -> password of the user
    """
    return model.check_user(username, password)
    