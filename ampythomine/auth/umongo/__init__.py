import asyncio

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

from umongo import Document, fields

from ...db.backends.umongo_motor import uMongoMotorBackend

register = uMongoMotorBackend().objects.register


@register
class User(Document):
    login = fields.StrField()
    password = fields.StrField()
    disabled = fields.BooleanField()
    is_superuser = fields.BooleanField()


@register
class Permission(Document):
    user = fields.ReferenceField(User)
    name = fields.StrField()


__auth_policy__ = 'uMongoAuthorizationPolicy'


class uMongoAuthorizationPolicy(AbstractAuthorizationPolicy):
    @asyncio.coroutine
    def authorized_userid(self, identity):
        return identity if (yield from User.count()) else None

    @asyncio.coroutine
    def permits(self, identity, permission, context=None):
        user = yield from User.find_one({"login": identity, "disabled": False})
        if identity is None or user is None:
            return False
        if user.is_superuser:
            return True
        for record in (yield from Permission.find({'user': user.id})):
            if record.name == permission:
                return True


@asyncio.coroutine
def check_credentials(username, password):
    user = yield from User.find_one({"login": username, "disabled": False})
    return sha256_crypt.verify(password, user.password) if user is not None else False
