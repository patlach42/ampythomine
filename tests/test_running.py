from aiohttp import web
from ampythomine import Application
from ampythomine.config import Config
import os


async def hello(request):
    return web.Response()


async def test_running(loop, test_server, test_client):
    config = Config(os.path.abspath('.'))
    config.from_pyfile('tests/tests.cfg')
    app = Application(loop=loop, config=config)

    app.router.add_get('/', hello)

    server = await test_server(app)
    client = await test_client(server)
    resp = await client.get('/')
    assert resp.status == 200
