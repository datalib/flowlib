class Engine(object):
    def __init__(self, start=(), mappers=(), reducers=()):
        self.start = list(start)
        self.mappers = list(mappers)
        self.reducers = list(reducers)

    @property
    def procs(self):
        rv = []
        rv.extend(self.start)
        rv.extend(self.mappers)
        rv.extend(self.reducers)
        return rv

    def transform(self, data):
        for stage in self.procs:
            data = stage(data)
        return data
