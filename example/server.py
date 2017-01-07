import os
import ampythomine
from ampythomine.config import Config
from aiohttp.web import run_app
import models

if __name__ == "__main__":
    config = Config(os.path.abspath('.'))
    config.from_pyfile('./tests.cfg')
    app = ampythomine.Application(config=config)
    run_app(app)
