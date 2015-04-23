from flowlib.core import branch, compose


class Stream(object):
    def __init__(self, func):
        self.func = func
        self.cls = self.__class__
        self.prevs = ()

    def clone(self, func, child=True):
        u = self.cls(func)
        u.prevs = self.prevs
        if child:
            u.prevs += (self,)
        return u

    def branch(self, fns):
        return self.clone(branch(self.func, to=fns),
                          child=False)

    def then(self, fn):
        return self.clone(fn)

    def __call__(self, data):
        fn = compose([p.func for p in self.prevs] + [self.func])
        return fn(data)
