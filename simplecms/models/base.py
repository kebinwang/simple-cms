import datetime

from peewee import Model
from simplecms import database

class BaseModel(Model):

    class Meta:
        database = database

    def save(self, *args, **kwargs):
        if hasattr(self, 'update_time'):
            self.update_time = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
