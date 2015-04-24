from functools import partial, wraps
from inspect import isgenerator
from .helpers import branch_generator, branch_reentrant


def pipeline(data, funcs):
    for stage in funcs:
        data = stage(data)
    return data


def branch(src, to):
    @wraps(src)
    def func(*args, **kwargs):
        it = src(*args, **kwargs)
        if isgenerator(it):
            return branch_generator(it, to)
        return branch_reentrant(it, to)
    return func


def compose(funcs):
    return partial(pipeline, funcs=funcs)


def each(fn):
    @wraps(fn)
    def function(stream):
        for item in stream:
            yield fn(item)
    return function
