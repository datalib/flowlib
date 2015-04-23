flowlib
=======

Library implementing primitives and utilities for making
data processing pipelines in a declarative way. The
simplest way of using the library::

    from flowlib.api import stream

    pipe = stream(fn1)
        .branch([stream(fn2),
                 stream(fn3).then(fn4)])\
        .then(fn5)\
        .then(fn6)
