from content import Post, Reply

def transformPostDataToObject(db_data: tuple) -> Post:
    post = Post(
        author_id = db_data[1],
        title = db_data[3],
        id = db_data[0],
        date = db_data[2],
        content = db_data[4],
        image = db_data[5]
    )
    return post

def transformReplyDataToObject(db_data: tuple) -> Reply:
    reply = Reply(
        id = db_data[0],
        author_id=db_data[1],
        parent_post_id=db_data[5],
        date = db_data[2],
        content=db_data[3],
        image=db_data[4]
    )
    return reply
    

    