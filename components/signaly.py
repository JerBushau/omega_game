import pygame
from collections import OrderedDict

class Signaly:
    def __init__(self):
        self.events = {}

    def emit(self, event_type):
        try:
            if self.events[event_type]['calls'] < self.events[event_type]['max_calls']:
                self.events[event_type]['calls'] += 1

            self.events[event_type]['callback']()

            if self.events[event_type]['calls'] >= self.events[event_type]['max_calls']:
                self.remove_subscriber(event_type)

        except KeyError:
            print('Invalid event type.')

    def subscribe(self, event_type, callback, max_calls=None):
        if max_calls != None:
            self.events[event_type] = { 'callback': callback, 'max_calls': max_calls, 'calls': 0 }
        else:
            self.events[event_type] = { 'callback': callback }

    def remove_subscriber(self, event_type):
        del self.events[event_type]



signaly = Signaly()
