from collections import defaultdict
from flowlib.exceptions import NoSuchEvent


class Engine(object):
    order = ('map', 'reduce')

    def __init__(self, **kwargs):
        self.procs = defaultdict(list, kwargs)
        self.event_hooks = {
            'post-map': self.procs['map'].append,
            'post-reduce': self.procs['reduce'].append,
        }

    def transform(self, data):
        for stage in self.order:
            for func in self.procs[stage]:
                data = func(data)
        return data

    def hook(self, event):
        if event not in self.event_hooks:
            raise NoSuchEvent(event)
        cb = self.event_hooks[event]
        def decorator(fn):
            cb(fn)
            return fn
        return decorator
