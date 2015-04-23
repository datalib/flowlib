from collections import defaultdict
from functools import wraps


def getargspec(f):
    if not hasattr(f, '__orgargs__'):
        code = f.__code__
        f.__orgargs__ = code.co_varnames[:code.co_argcount]
    return f.__orgargs__


def already_resolved(argspec, pos, kwd):
    resolved = set(name for name, _ in zip(argspec, pos))
    resolved.update(kwd)
    return resolved


def resolve_deps(deps, exclude):
    for name, cb in deps:
        if name not in exclude:
            yield name, cb()


class Injector(object):
    def __init__(self):
        self.registry = {}

    def provides(self, name):
        def decorator(fn):
            self.registry[name] = fn
            return fn
        return decorator

    def requires(self, *names):
        def decorator(fn):
            deps = [(k, self.registry[k]) for k in names]
            names = getargspec(fn)

            @wraps(fn)
            def func(*args, **kwargs):
                resolved = already_resolved(names, args, kwargs)
                kwargs.update(resolve_deps(deps, exclude=resolved))
                return fn(*args, **kwargs)
            return func
        return decorator
