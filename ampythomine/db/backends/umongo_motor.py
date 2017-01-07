from .abc import DatabaseBackend
from umongo import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient

__backend__ = 'uMongoMotorBackend'


class uMongoMotorBackend(DatabaseBackend):
    objects = MotorAsyncIOInstance()

    def init(self, config):
        self.objects.init(AsyncIOMotorClient()[config['NAME']])
