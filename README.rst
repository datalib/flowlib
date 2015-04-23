flowlib
=======

Declarative data processing pipeline framework for Python,
with support for dependency injection to make it easier to
create testable, functional and working pipelines::

    from flowlib.engine import Engine

    def add(data):
        return sum(data)

    engine = Engine([add])
    assert engine.transform([1,2,3]) == 6
