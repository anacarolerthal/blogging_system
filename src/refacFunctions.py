from utils import *
from model import BlogModel

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


        
        