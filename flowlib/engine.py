from collections import defaultdict
from flowlib.exceptions import NoSuchEvent
from flowlib.core import pipeline


class Engine(object):
    order = ('map', 'reduce')

    def __init__(self, **kwargs):
        self.procs = defaultdict(list, kwargs)
        self.event_hooks = {
            'post-%s' % (stage,): self.procs[stage].append
            for stage in self.order
        }

    def compile_pipeline(self):
        procs = []
        for stage in self.order:
            procs.extend(self.procs[stage])
        return procs

    def transform(self, data):
        return pipeline(data,
                        self.compile_pipeline())

    def hook(self, event):
        def decorator(fn):
            self.register_hook(event, fn)
            return fn
        return decorator

    def register_hook(self, event, fn):
        if event not in self.event_hooks:
            raise NoSuchEvent(event)
        handler = self.event_hooks[event]
        handler(fn)
