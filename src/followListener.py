from event import subscribe
from users import User

def handle_follow_event(follower: User, followee: User):
    print(f"{follower.username} start to following you, {followee.email}")

def setup_follow_event():
    subscribe("follow", handle_follow_event)
