from model import BlogModel
from utils import *

def getTaggedPosts(model: BlogModel, user_id: int = None) -> list:
    """
    Returns a list of posts with tag. If user_id is provided, returns only posts by that user.
    """
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

def getUserInstanceWithUsername(model: BlogModel, user_id: int) -> User:
    """
    Returns a User instance for the user with user_id.
    """
    username = model.get_username_by_user_id(user_id)
    user = User(username=username)
    user.set_id(user_id)
    return user

def getUserFollowers(model: BlogModel, user_id: int) -> list:
    """
    Returns a list of users who follow the user with user_id.
    """
    user = getUserInstanceWithUsername(model, user_id)
    followers = user.get_followers()
    return user, followers