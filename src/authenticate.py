import model

model = model.BlogModel()


def authenticate(username, password):
    """Authenticate a user
    
    username: str -> username of the user
    password: str -> password of the user
    """
    print("oi \n")
    print(username + "\n")
    print(password)
    return model.check_user(username, password)
    