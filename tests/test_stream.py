import pytest
from flowlib.stream import Stream
from flowlib.core import each


@pytest.fixture
def stream():
    return Stream(lambda x: [(k + 1) for k in x])


def test_stream_single_call(stream):
    assert stream([1,2,3]) == [2,3,4]


def test_stream_then(stream):
    for n in range(1, 5):
        factor = 2 ** n
        stream = stream.then(lambda x: [k*2 for k in x])
        assert stream([1,2,3]) == [(k * factor) for k in [2,3,4]]


def test_stream_immutable(stream):
    g = stream.then(lambda x: x)
    assert stream is not g
    assert stream in g.prev


@pytest.fixture
def branch(stream):
    ctx = []
    stream = stream.branch([
        Stream(ctx.extend),
        Stream(ctx.extend).then(ctx.append),
    ])
    return stream, ctx


def test_branching_returns_main_stream(branch):
    stream, _ = branch
    assert list(stream([1,2,3])) == [2,3,4]


def test_branching_calls_other_streams(branch):
    stream, ctx = branch
    stream([1,2,3])
    assert ctx == [2,3,4,2,3,4,None]
