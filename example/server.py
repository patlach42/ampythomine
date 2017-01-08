import os
import ampythomine
from ampythomine.config import Config
from ampythomine.web import View
from ampythomine.auth.umongo.views import uMongoAuthLogin, uMongoAuthLogout
from ampythomine.auth import require

from aiohttp.web import run_app
import models


class Index(View):
    @require('public')
    async def get(self, request):
        return self.response('')


if __name__ == "__main__":
    config = Config(os.path.abspath('.'))
    config.from_pyfile('./tests.cfg')
    app = ampythomine.Application(config=config, routes=[
        ('GET', '/', Index),
        ('POST', '/l', uMongoAuthLogin),
        ('POST', '/q', uMongoAuthLogout)
    ])
    run_app(app)
