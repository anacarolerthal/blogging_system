from model import BlogModel
from utils import *

def returnPostsToMainPage(model: BlogModel) -> list:
    posts = [transformPostDataToObject(post) for post in model.get_all_posts()]
    # get post tags
    tagged_posts =[]
    for post in posts:
        tag_ids = model.get_tags_for_post(post.id)
        # get tag names from tag ids
        tags = []
        for tag_id in tag_ids:
            tags.append(model.get_tag_name_by_id(tag_id))
        # add tags to post
        post.tags = tags
        tagged_posts.append(post)
    tagged_posts.reverse()
    return tagged_posts

def returnTaggedUserPosts(model: BlogModel, user_id: int) -> list:
    user_posts = [transformPostDataToObject(post) for post in model.get_posts_for_user(user_id)]
    tagged_user_posts =[]
    # get post tags
    for post in user_posts:
        tag_ids = model.get_tags_for_post(post.id)
        # get tag names from tag ids
        tags = []
        for tag_id in tag_ids:
            tags.append(model.get_tag_name_by_id(tag_id))
        # add tags to post
        post.tags = tags
        tagged_user_posts.append(post)
    tagged_user_posts.reverse()
    return tagged_user_posts