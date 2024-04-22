from models import Vehicle
from response import Response


class Middleware:
    def pre(self, *args, **kwargs):
        return

    def post(self, *args, **kwargs):
        return


class MiddlewareDecorator:
    def use(self, mw: Middleware, pre=False, post=True):
        attrs = self.__class__.__dict__

        for attr in attrs:
            if callable(attrs[attr]):
                def decorator(function):
                    def wrapper(*args, **kwargs):
                        if pre:
                            r = mw.pre(*args, function=function, **kwargs)
                            if r is not None:
                                return r
                        r = function.__call__(self, *args, **kwargs)
                        if post:
                            mw.post(*args, result=r, function=function)
                        return r

                    return wrapper

                setattr(self, attr, decorator(attrs[attr]))


class APIMiddleware(Middleware):
    def __init__(self):
        self.cache = {}

    def pre(self, *args, **kwargs):
        name = kwargs['function'].__name__

        if name == 'get':
            if len(args):
                r = self.cache.get(args[0])
                if not r and self.cache.get(-1) is not None:
                    for it in self.cache.get(-1).data:
                        if it.id == args[0]:
                            return Response(instance=it)
            else:
                return self.cache.get(-1)

    def post(self, *args, **kwargs):
        name = kwargs['function'].__name__

        if name == 'get':
            if not len(args): args = [-1]
            self.cache[args[0]] = kwargs['result']


class ManagerMiddleware(Middleware):
    def post(self, *args, **kwargs):
        result = kwargs['result']
        name = kwargs['function'].__name__
        if name in ['update']:
            return
        print(name, args, end=' ')
        if isinstance(result, list):
            print(*[it.json() for it in result])
        elif isinstance(result, Vehicle):
            print(result.json())
        else:
            print(result)
