from inspect import isgenerator
from functools import partial, wraps
from itertools import tee


def pipeline(data, funcs):
    for stage in funcs:
        data = stage(data)
    return data


def branch_generator(it, to):
    streams = tee(it, len(to)+1)
    emit, streams = stream[0], streams[1:]
    for stream, consumer in zip(streams, to):
        consumer(stream)
    return emit


def branch_reentrant(it, to):
    for consumer in to:
        consumer(it)
    return it


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
