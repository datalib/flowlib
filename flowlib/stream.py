from flowlib.core import branch, compose


class Stream(object):
    def __init__(self, func):
        self.func = func
        self.prev = ()

    def clone(self, func, child=True):
        u = self.__class__(func)
        u.prev = self.prev
        if child:
            u.prev += (self,)
        return u

    def branch(self, fns):
        return self.clone(branch(self.func, to=fns),
                          child=False)

    def then(self, fn):
        return self.clone(fn)

    def __call__(self, data):
        fn = compose([p.func for p in self.prev] + [self.func])
        return fn(data)

    @classmethod
    def from_iterable(cls, funcs):
        funcs = iter(funcs)
        stream = cls(next(funcs))
        for proc in funcs:
            stream = stream.then(proc)
        return stream
