import asyncio
import functools
from aiohttp_security import permits
from aiohttp import web

def require(permission):
    def wrapper(f):
        @asyncio.coroutine
        @functools.wraps(f)
        def wrapped(self, *args):
            has_perm = yield from permits(self.request, permission)
            if not has_perm:
                message = 'User has no permission {}'.format(permission)
                raise web.HTTPForbidden(body=message.encode())
            return (yield from f(self, self.request))
        return wrapped
    return wrapper