#subscribers = dict()

# def subscribe(event_type: str, fn) -> None:
#     if not event_type in subscribers:
#         subscribers[event_type] = []
#     subscribers[event_type].append(fn)

# def post_event(event_type: str, data):
#     if not event_type in subscribe:
#         return
#     for fn in subscribers[event_type]:
#         fn(data)

class Event():
    #self.subscribers = dict()
    def __init__(self):    
        self.subscribers = dict()

    def subscribe(self, event_type: str, fn) -> None:
        if not event_type in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)

    def post_event(self, event_type: str, data):
        if not event_type in self.subscribe:
            return
        for fn in self.subscribers[event_type]:
            fn(data)
