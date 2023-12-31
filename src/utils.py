from content import Post, Reply
from users import User

def transformPostDataToObject(db_data: tuple) -> Post:
    post = Post(
        author_id = db_data[1],
        title = db_data[3],
        id = db_data[0],
        date = db_data[2],
        content = db_data[4]
    )
    return post

def transformReplyDataToObject(db_data: tuple) -> Reply:
    reply = Reply(
        id = db_data[0],
        author_id=db_data[1],
        parent_post_id=db_data[5],
        date = db_data[2],
        content=db_data[3]
    )
    return reply
    
def transformUserDataToObject(db_data: tuple) -> User:
    user = User(
        id = db_data[0],
        username=db_data[1],
        password=db_data[5],
        email = db_data[2],
        posts=None,
        followers=None,
        following=None
    )
    return user
    

    