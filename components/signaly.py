import pygame

class Signaly:
    def __init__(self):
        self.events = {}

    def emit(self, event_type, payload=None):
        try:
            event = self.events[event_type]
        except KeyError:
            print('Invalid event type.')

        if payload:
            event['callback'](payload)
        else:
            event['callback']()

        if event['max_calls']:
            event['calls'] += 1

        if event['max_calls'] and event['calls'] >= event['max_calls']:
            self.remove_subscriber(event_type)

    def subscribe(self, event_type, callback, max_calls=0):
        self.events[event_type] = { 'callback': callback,
                                    'max_calls': max_calls,
                                    'calls': 0 }

    def remove_subscriber(self, event_type):
        del self.events[event_type]



signaly = Signaly()
