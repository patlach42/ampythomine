import asyncio

from aiohttp import web, hdrs

from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.abc import AbstractView

from json import dumps


class View(AbstractView):
    @asyncio.coroutine
    def __iter__(self):
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        resp = yield from self.dispatch()
        return resp

    def __await__(self):
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        resp = yield from self.dispatch()
        return resp

    def _raise_allowed_methods(self):
        allowed_methods = {
            m for m in hdrs.METH_ALL if hasattr(self, m.lower())}
        raise HTTPMethodNotAllowed(self.request.method, allowed_methods)

    @asyncio.coroutine
    def dispatch(self):
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        resp = yield from method()
        return resp

    @staticmethod
    def response(body, content_type='text/html', charset='utf-8', status_code=200):
        kwargs = {'body': body, 'content_type': content_type, 'charset': charset, 'status': status_code}
        if isinstance(body, str):
            kwargs['body'] = body.encode('utf-8')
        elif isinstance(body, dict) or isinstance(body, list):
            kwargs['content_type'] = 'application/json'
            kwargs['body'] = dumps(body).encode('utf-8')
        elif isinstance(body, int) or isinstance(body, float):
            kwargs['body'] = str(body).encode('utf-8')
        return web.Response(**kwargs)
