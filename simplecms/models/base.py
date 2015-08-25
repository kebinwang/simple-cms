import datetime

from peewee import Model, DateTimeField
from simplecms import database

class BaseModel(Model):
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
