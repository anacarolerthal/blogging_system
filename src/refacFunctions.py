from utils import *
from model import BlogModel
from users import UserFactory
from tags import Tag
from admin import Admin
import re

def getTaggedPosts(model: BlogModel, user_id: int = None) -> list:
    if user_id is None:
        posts = [transformPostDataToObject(post) for post in model.get_all_posts()]
    else:
        posts = [transformPostDataToObject(post) for post in model.get_posts_for_user(user_id)]
    
    # get post tags
    tagged_posts =[]
    
    for post in posts:
        tag_ids = model.get_tags_for_post(post.id)
        # get tag names from tag ids
        tags = []
        
        for tag_id in tag_ids:
            if tag_id is not None:
                tags.append(model.get_tag_name_by_id(tag_id))
        
        # add tags to post
        post.tags = tags
        tagged_posts.append(post)
        
    tagged_posts.reverse()
    return tagged_posts

def getPostsByPostID(model: BlogModel, tag: str) -> list:
    tag_id = model.get_tag_id_by_name(tag)
    post_ids = model.get_post_id_by_tag(tag_id)
    posts = []
    
    for post_id in post_ids:
        posts.append(transformPostDataToObject(model.get_post_by_post_id(post_id)))
        
    tagged_posts = []
    for post in posts:
        tag_ids = model.get_tags_for_post(post.id)
        tags = []
        for tag_id in tag_ids:
            if tag_id is not None:
                tags.append(model.get_tag_name_by_id(tag_id))
                
        post.tags = tags
        tagged_posts.append(post)
    
    tagged_posts.reverse()
    return tagged_posts

def getUserAndFollowers(model: BlogModel, user_id: int) -> tuple:
    username = model.get_username_by_id(user_id)
    user = UserFactory().create_user("USER", username, user_id)
    user.set_id(user_id)
    followers = user.get_followers()
    return user, followers

def splitTags(tags: str) -> list:
    """
    Returns a list of tags from a string of tags.
    """
    post_tags = []
    for tag in tags.split():
        tg = Tag(tag_name=tag)
        tg.publish()
        post_tags.append(tag)
    return post_tags

def createPostWithSplitTags(user_id: int, title: str, content: str, post_tags: list) -> Post:
    """
    Creates a post with tags from a string of tags.
    """
    post = Post(
        author_id=user_id,
        title=title,
        content=content,
        tags=post_tags
    )
    return post

def createReplyWithPostID(user_id: int, post_id: int, content: str) -> Reply:
    """
    Creates a comment with the post_id.
    """
    reply = Reply(
        author_id=user_id,
        content=content,
        parent_post_id=post_id
    )
    query_string = "post_id={}".format(post_id)
    return reply, query_string

def getComments(model: BlogModel, post_id: int) -> list:
    """
    Returns a list of comments for a post.
    """
    pattern = r'(?<==)([^=\s]+)' #The "postId" parameter is in the format "postId=8", so use regex to extract the 8
    matches = re.findall(pattern, post_id)
    id = int(matches[0])
    comments = model.get_comments_for_post(id)
    return comments

def getCommentsObjects(comments: list) -> list:
    """
    Returns a list of comment objects for a post.
    """
    comments_objects = [transformReplyDataToObject(comment) for comment in comments]
    comments_objects.reverse()
    return comments_objects