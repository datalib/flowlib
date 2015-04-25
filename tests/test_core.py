import pytest
from flowlib.core import pipeline, branch, compose, each


def test_each():
    f = each(lambda x: x+1)
    assert list(f([1,2,3])) == [2,3,4]


def test_pipeline():
    funcs = [
        lambda x: x+1,
        lambda x: x+2,
        lambda x: x+3,
    ]
    assert pipeline(0, funcs) == 6
    assert pipeline(1, funcs) == 7


def test_compose():
    f = lambda x: x+1
    g = lambda x: x+2

    fg = compose([f, g])
    assert fg(1) == 4
    assert fg(2) == 5


def test_branch():
    ctx = []
    u = branch((k for k in [1,2]),
               [
                   ctx.extend,
                   ctx.extend,
               ])
    assert list(u) == [1,2]
    assert ctx == [1,2,1,2]
