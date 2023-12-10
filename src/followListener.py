from event import Event

def handle_follow_event():
    print(f"You receveid a new follow!")

def setup_follow_event(event: Event):
    event.subscribe("follow", handle_follow_event)
