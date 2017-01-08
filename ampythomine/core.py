import os
import asyncio
import logging
import importlib

import uvloop

from aiohttp.web import Application as AioHTTPApp

import aiohttp_jinja2
import jinja2

from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from .auth.identity import IdentityPolicy
from aioredis import Redis, RedisPool


class Application(AioHTTPApp):
    def __init__(self, *args, config=None, routes=[], **kwargs):
        self.logger = logging.getLogger('ampythomine')
        self.jinja = aiohttp_jinja2
        super().__init__(*args, **kwargs)
        self.jinja.setup(self,
                         loader=jinja2.FileSystemLoader(os.path.abspath(config['TEMPLATE_PATH'])))
        for route in routes:
            self.router.add_route(route[0], route[1], route[2])
        # Database init
        db_backend = importlib.import_module(config['DATABASE']['BACKEND'])
        getattr(db_backend, db_backend.__backend__)().init(config['DATABASE'])

        # Auth init
        # TODO: подтягивать бэкэнд для хранения сессий из конфига
        redis_pool = RedisPool(('localhost', 6379), db=0, password=None, ssl=None, encoding=None,
                               minsize=1, maxsize=10, commands_factory=Redis, loop=None)
        setup_session(self, RedisStorage(redis_pool))
        auth_backend = importlib.import_module(config['AUTH']['BACKEND'])
        setup_security(self,
                       IdentityPolicy(),
                       getattr(auth_backend, auth_backend.__auth_policy__)())
