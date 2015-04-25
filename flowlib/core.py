from functools import partial, wraps
from itertools import tee


def pipeline(data, funcs):
    for stage in funcs:
        data = stage(data)
    return data


def branch(src, to):
    streams = tee(src, len(to) + 1)
    emit, streams = streams[0], streams[1:]

    for stream, consumer in zip(streams, to):
        consumer(stream)
    return emit


def compose(funcs):
    return partial(pipeline, funcs=funcs)


def each(fn):
    @wraps(fn)
    def function(stream):
        for item in stream:
            yield fn(item)
    return function
