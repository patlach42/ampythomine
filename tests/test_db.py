from ampythomine import Application
from ampythomine.config import Config
from umongo import Document, fields
import os

from ampythomine.db.backends.umongo_motor import uMongoMotorBackend
objects = uMongoMotorBackend().objects


@objects.register
class Some(Document):
    citizenship = fields.StrField()  # Гражданство
    destination_country = fields.StrField()  # Страна назначения
    document = fields.StrField()  # Необходимый документ
    fields_groups = fields.ListField(fields.DictField())
    fields = fields.ListField(fields.DictField())


async def test_db(loop, test_server, test_client):
    config = Config(os.path.abspath('.'))
    config.from_pyfile('tests/tests.cfg')
    app = Application(loop=loop, config=config)
    assert Some.find_one()
