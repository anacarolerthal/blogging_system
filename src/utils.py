from content import Post, Reply

def transformPostDataToObject(db_data: tuple) -> Post:
    post = Post(
        author_id = int(db_data[1]),
        title = str(db_data[3]),
        id = int(db_data[0]),
        date = str(db_data[2]),
        content = str(db_data[4]),
        image = str(db_data[5])
    )
    return post


# def transformReplyDataToObject(db_data: tuple) -> Reply():
#     reply = ContentFactory.get_content("REPLY")
#     reply.id = db_data[0]
#     reply.author_id = db_data[1]
#     reply.date = db_data[2]
#     reply.content = db_data[3]
#     reply.image = db_data[4]
#     reply.parent_post_id = db_data[5]
    

    