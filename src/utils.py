from content import Post, Reply, ContentFactory

def transformPostDataToObject(db_data: tuple) -> Post():
    post = ContentFactory.get_content("POST")
    post.id = db_data[0]
    post.author_id = db_data[1]
    post.date = db_data[2]
    post.title = db_data[3]
    post.content = db_data[4]
    post.image = db_data[5]

def transformReplyDataToObject(db_data: tuple) -> Reply():
    reply = ContentFactory.get_content("REPLY")
    reply.id = db_data[0]
    reply.author_id = db_data[1]
    reply.date = db_data[2]
    reply.content = db_data[3]
    reply.image = db_data[4]
    reply.parent_post_id = db_data[5]
    

    