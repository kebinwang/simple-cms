from peewee import Model
from simplecms import database

class BaseModel(Model):
    class Meta:
        database = database
