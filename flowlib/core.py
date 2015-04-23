from functools import partial, wraps
from itertools import tee


def pipeline(data, funcs):
    for stage in funcs:
        data = stage(data)
    return data


def branch(src, to):
    num_of_streams = len(to) + 1

    @wraps(src)
    def func(*args, **kwargs):
        it = src(*args, **kwargs)
        streams = tee(it, num_of_streams)

        emit, streams = streams[0], streams[1:]
        for consumer, stream in zip(to, streams):
            for item in consumer(stream):
                pass
        return emit
    return func


def compose(funcs):
    return partial(pipeline, funcs=funcs)


def each(fn):
    @wraps(fn)
    def function(stream):
        for item in stream:
            yield fn(item)
    return function
