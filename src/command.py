from abc import ABC, abstractmethod
from singleton import Singleton

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DBCommand(Command):
    def __init__(self, db_connection):
        self.connection = db_connection
        self.cursor = self.connection.cursor()

class CreatePostCommand(DBCommand):
    def __init__(self, db_connection, post):
        super().__init__(db_connection)
        self.post = post

    def execute(self):
        self.cursor.execute('INSERT INTO Post (author_id, title, text_content) VALUES (%s, %s, %s) RETURNING id',
                       (self.post.author_id, self.post.title, self.post.content))
        id = self.cursor.fetchone()[0]
        self.connection.commit()
        return id
    
class CreateTaggedPost(DBCommand):
    def __init__(self, db_connection, post_id, tag_id):
        super().__init__(db_connection)
        self.post_id = post_id
        self.tag_id = tag_id

    def execute(self):
        self.cursor.execute('INSERT INTO posttag (post_id, tag_id) VALUES (%s,%s)', (self.post_id, self.tag_id))
        self.connection.commit()    

class CreateReplyCommand(DBCommand):
    def __init__(self, db_connection, reply):
        super().__init__(db_connection)
        self.reply = reply

    def execute(self):
        self.cursor.execute('INSERT INTO Reply (author_id, text_content, parent_post_id) VALUES (%s, %s, %s) RETURNING id', 
                            (self.reply.author_id, self.reply.content, self.reply.parent_post_id))
        id = self.cursor.fetchone()[0]
        self.connection.commit()
        return id
    
class CreateUserCommand(DBCommand):
    def __init__(self, db_connection, username, password, email, is_moderator):
        super().__init__(db_connection)
        self.username = username
        self.password = password
        self.email = email
        self.is_moderator = is_moderator
    
    def execute(self):
        self.cursor.execute('INSERT INTO baseuser (username, passw, email, is_moderator) VALUES (%s, %s, %s, %s) RETURNING id', (self.username, self.password, self.email, self.is_moderator))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return user_id
    
class CreateFollowCommand(DBCommand):
    def __init__(self, db_connection, follower, followee):
        super().__init__(db_connection)
        self.follower = follower
        self.followee = followee
    
    def execute(self):
        self.cursor.execute('INSERT INTO userfollows (follower_id, followee_id) VALUES (%s,%s)', (self.follower, self.followee))
        self.connection.commit()

class CreateLikeCommand(DBCommand):
    def __init__(self, db_connection, user_id, post_id):
        super().__init__(db_connection)
        self.user_id = user_id
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('INSERT INTO postlikes (user_id, post_id) VALUES (%s,%s)', (self.user_id, self.post_id))
        self.connection.commit()

class CreateTag(DBCommand):
    def __init__(self, db_connection, tag_name):
        super().__init__(db_connection)
        self.tag_name = tag_name

    def execute(self):
        self.cursor.execute('INSERT INTO tag (tag_name) VALUES (%s) RETURNING tag_id', (self.tag_name,))
        tag_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return tag_id      

class DeleteLikeCommand(DBCommand):
    def __init__(self, db_connection, user_id, post_id):
        super().__init__(db_connection)
        self.user_id = user_id
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('DELETE FROM postlikes WHERE user_id = %s AND post_id = %s', (self.user_id, self.post_id))
        self.connection.commit()

class DeleteFollowCommand(DBCommand):
    def __init__(self, db_connection, follower, followee):
        super().__init__(db_connection)
        self.follower = follower
        self.followee = followee
    
    def execute(self):
        self.cursor.execute('DELETE FROM userfollows WHERE follower_id = %s AND followee_id = %s', (self.follower, self.followee))
        self.connection.commit()  

class GetTagsByPost(DBCommand):
    def __init__(self, db_connection, post_id):
        super().__init__(db_connection)
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('SELECT tag_id FROM posttag WHERE post_id = %s', (self.post_id,))
        out = self.cursor.fetchall()
        tag_id_list = []
        for tag_id in out:
            tag_id_list.append(tag_id[0])
        return tag_id_list
    
class GetTagNameById(DBCommand):
    def __init__(self, db_connection, tag_id):
        super().__init__(db_connection)
        self.tag_id = tag_id

    def execute(self):
        self.cursor.execute('SELECT tag_name FROM tag WHERE tag_id = %s', (self.tag_id,))
        return self.cursor.fetchone()[0]

class GetTagIdByName(DBCommand):
    def __init__(self, db_connection, tag_name):
        super().__init__(db_connection)
        self.tag_name = tag_name

    def execute(self):
        self.cursor.execute('SELECT tag_id FROM tag WHERE tag_name = %s', (self.tag_name,))
        return int(self.cursor.fetchone()[0])

class GetAllPostsCommand(DBCommand):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def execute(self):
        self.cursor.execute('SELECT * FROM Post')
        return self.cursor.fetchall()

class GetPostsLikedByUser(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT post_id FROM postlikes WHERE user_id = %s', (self.user_id,))
        out = self.cursor.fetchall()
        id_lists = []
        for id in out:
            id_lists.append(id[0])
        return id_lists

class GetPostsFromUserCommand(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT * FROM Post WHERE author_id = %s', (self.user_id,))
        return self.cursor.fetchall()

class GetCommentsOfPostCommand(DBCommand):
    def __init__(self, db_connection, postId):
        super().__init__(db_connection)
        self.postId = postId

    def execute(self):
        self.cursor.execute('SELECT * FROM Reply WHERE parent_post_id = %s', (self.postId,))
        return self.cursor.fetchall()

class GetFollowingUsersByUserId(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT followee_id FROM userfollows WHERE follower_id = %s', (self.user_id,))
        out = self.cursor.fetchall()
        id_lists = []
        for id in out:
            id_lists.append(id[0])
        return id_lists

class GetFollowerUsersByUserId(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT follower_id FROM userfollows WHERE followee_id = %s', (self.user_id,))
        out = self.cursor.fetchall()
        id_lists = []
        for id in out:
            id_lists.append(id[0])
        return id_lists


class CheckUserCommand(DBCommand):
    def __init__(self, db_connection, username, password):
        super().__init__(db_connection)
        self.username = username
        self.password = password

    def execute(self):
        self.cursor.execute('SELECT * FROM baseuser WHERE username = %s AND passw = %s', (self.username, self.password))
        return bool(self.cursor.fetchone())

class CheckUserInDBCommand(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT * FROM baseuser WHERE id = %s', (self.user_id,))
        return bool(self.cursor.fetchone())

class CheckPostInDbCommand(DBCommand):
    def __init__(self, db_connection, post_id):
        super().__init__(db_connection)
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('SELECT * FROM post WHERE id = %s', (self.post_id,))
        return bool(self.cursor.fetchone())

class CheckPostAlreadyLiked(DBCommand):
    def __init__(self, db_connection, user_id, post_id):
        super().__init__(db_connection)
        self.user_id = user_id
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('SELECT * FROM postlikes WHERE user_id = %s AND post_id = %s', (self.user_id, self.post_id))
        return bool(self.cursor.fetchone())

class CheckTagAlreadyInDB(DBCommand):
    def __init__(self, db_connection, tag_name):
        super().__init__(db_connection)
        self.tag_name=tag_name

    def execute(self):
        self.cursor.execute('SELECT * FROM tag WHERE tag_name = %s', (self.tag_name,))
        return bool(self.cursor.fetchone())

class GetUserIdByUsernameCommand(DBCommand):
    def __init__(self, db_connection, username):
        super().__init__(db_connection)
        self.username = username

    def execute(self):
        self.cursor.execute('SELECT id FROM baseuser WHERE username = %s', (self.username,))
        return int(self.cursor.fetchone()[0])

class GetUsernameByUserIdCommand(DBCommand):
    def __init__(self, db_connection, user_id):
        super().__init__(db_connection)
        self.user_id = user_id

    def execute(self):
        self.cursor.execute('SELECT username FROM baseuser WHERE id = %s', (self.user_id,))
        return self.cursor.fetchone()
    
class GetTagIdByNameCommand(DBCommand):
    def __init__(self, db_connection, tag_name):
        super().__init__(db_connection)
        self.tag_name = tag_name

    def execute(self):
        self.cursor.execute('SELECT tag_id FROM tag WHERE tag_name = %s', (self.tag_name,))
        return int(self.cursor.fetchone()[0])
    
class GetPostIdByTagIdCommand(DBCommand):
    def __init__(self, db_connection, tag_id):
        super().__init__(db_connection)
        self.tag_id = tag_id

    def execute(self):
        self.cursor.execute('SELECT post_id FROM posttag WHERE tag_id = %s', (self.tag_id,))
        out = self.cursor.fetchall()
        post_id_list = []
        for post_id in out:
            post_id_list.append(post_id)
        return post_id_list

class GetPostByPostIdCommand(DBCommand):
    def __init__(self, db_connection, post_id):
        super().__init__(db_connection)
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('SELECT * FROM post WHERE id = %s', (self.post_id,))
        return self.cursor.fetchone()
    
class GetUserByUserIdCommand(DBCommand):
    def __init__(self, db_connection, id):
        super().__init__(db_connection)
        self.id = id

    def execute(self):
        self.cursor.execute('SELECT * FROM baseuser WHERE id = %s', (self.id, ))
        return self.cursor.fetchone()[0]

class CheckIfUserIsBannedCommand(DBCommand):
    def __init__(self, db_connection, id):
        super().__init__(db_connection)
        self.id = id

    def execute(self):
        self.cursor.execute('SELECT ban_id FROM bannedusers WHERE banned_id = %s', (self.id,))
        return bool(self.cursor.fetchone())

class BanUserCommand(DBCommand):
    def __init__(self, db_connection, banner_id, banned_id):
        super().__init__(db_connection)
        self.banner_id = banner_id
        self.banned_id = banned_id

    def execute(self):
        self.cursor.execute('INSERT INTO bannedusers (banner_id, banned_id) VALUES (%s, %s)', (self.banner_id, self.banned_id))
        self.connection.commit()

class UnbanUserCommand(DBCommand):
    def __init__(self, db_connection, banner_id, banned_id):
        super().__init__(db_connection)
        self.banner_id = banner_id
        self.banned_id = banned_id

    def execute(self):
        self.cursor.execute('DELETE FROM bannedusers WHERE banner_id = %s AND banned_id = %s', (self.banner_id, self.banned_id))
        self.connection.commit()

class DeletePostCommand(DBCommand):
    def __init__(self, db_connection, post_id):
        super().__init__(db_connection)
        self.post_id = post_id

    def execute(self):
        self.cursor.execute('DELETE FROM postlikes WHERE post_id = %s', (self.post_id,))
        self.cursor.execute('DELETE FROM posttag WHERE post_id = %s', (self.post_id,))
        self.cursor.execute('DELETE FROM reply WHERE parent_post_id = %s', (self.post_id,))
        self.cursor.execute('DELETE FROM post WHERE id = %s', (self.post_id,))
        self.connection.commit()

class CheckIfModeratorCommand(DBCommand):
    def __init__(self, db_connection, username):
        super().__init__(db_connection)
        self.username = username

    def execute(self):
        self.cursor.execute('SELECT is_moderator FROM baseuser WHERE username = %s', (self.username,))
        return bool(self.cursor.fetchone()[0])
