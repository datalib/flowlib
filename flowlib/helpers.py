from itertools import tee


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
