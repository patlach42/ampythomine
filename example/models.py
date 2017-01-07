from ampythomine.db.backends.umongo_motor import uMongoMotorBackend
from umongo import Document, fields

register = uMongoMotorBackend().objects.register


@register
class Some(Document):
    citizenship = fields.StrField()  # Гражданство
    destination_country = fields.StrField()  # Страна назначения
    document = fields.StrField()  # Необходимый документ
    fields_groups = fields.ListField(fields.DictField())
    fields = fields.ListField(fields.DictField())
