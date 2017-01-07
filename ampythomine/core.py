import os
import asyncio
import logging
import importlib

import uvloop

from aiohttp.web import Application as AioHTTPApp

import aiohttp_jinja2
import jinja2


class Application(AioHTTPApp):
    def __init__(self, *args, config=None, routes=[], **kwargs):
        self.logger = logging.getLogger('ampythomine')
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.jinja = aiohttp_jinja2
        super().__init__(*args, **kwargs)
        self.jinja.setup(self,
                         loader=jinja2.FileSystemLoader(os.path.abspath(config['TEMPLATE_PATH'])))
        for route in routes:
            self.router.add_route(route[0], route[1], route[2])
        # Database init
        db_backend = importlib.import_module(config['DATABASE']['BACKEND'])
        getattr(db_backend, db_backend.__backend__)().init(config['DATABASE'])
