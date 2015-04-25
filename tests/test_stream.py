import pytest
from flowlib.stream import Stream


@pytest.fixture
def stream():
    return Stream(lambda x: [(k + 1) for k in x])


def test_stream_single_call(stream):
    assert stream([1,2]) == [2,3]


def test_stream_then(stream):
    for n in range(1, 5):
        factor = 2 ** n
        stream = stream.then(lambda x: [k*2 for k in x])
        assert stream([1,2]) == [(k * factor) for k in [2,3]]


def test_stream_immutable(stream):
    g = stream.then(lambda x: x)
    assert stream is not g
    assert stream in g.prev


def test_stream_clone_inherit(stream):
    u = stream.clone(lambda x: [(k+2) for k in x])
    assert stream in u.prev
    assert stream([1,2]) == [2,3]
    assert u([1,2]) == [4,5]


def test_stream_clone_no_inherit(stream):
    u = stream.clone(lambda x: [(k+2) for k in x], inherit=False)
    assert stream not in u.prev
    assert u([1,2]) == [3,4]


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
    assert list(stream([1,2])) == [2,3]


def test_branching_calls_other_streams(branch):
    stream, ctx = branch
    stream([1,2])
    assert ctx == [2,3,2,3,None]


def test_stream_from_iterable():
    f = Stream.from_iterable([
        lambda x: x + [1],
        lambda k: k + [2],
        lambda z: z + [3],
    ])
    assert f([]) == [1,2,3]
