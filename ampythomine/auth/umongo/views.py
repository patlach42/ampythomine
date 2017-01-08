import asyncio
from aiohttp_security import remember
from ...web import View
from . import check_credentials
from aiohttp_security import remember, forget


class uMongoAuthLogin(View):
    @asyncio.coroutine
    def post(self):
        json = yield from self.request.json()
        login = json.get('login')
        password = json.get('password')
        response = self.response('')
        if (yield from check_credentials(login, password)):
            yield from remember(self.request, response, login)
            return response
        return response


class uMongoAuthLogout(View):
    @asyncio.coroutine
    def post(self):
        response = self.response('')
        yield from forget(self.request, response)
        return response