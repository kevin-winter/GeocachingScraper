from peewee import *

db = SqliteDatabase('geocaching.db')

class BaseModel(Model):
    class Meta:
        database = db


class Cache(BaseModel):
    id = CharField(primary_key=True)
    name = CharField(unique=True)
    difficulty = IntegerField()
    terrain = IntegerField
    size = IntegerField()
    lat = DecimalField()
    lon = DecimalField()
    creator = ForeignKeyField(User)


class User(BaseModel):
    username = CharField(primary_key=True)
    AccountGuid = CharField()
    AccountID = CharField()
    Email = CharField()
    GeocacheFindCount = IntegerField()
    GeocacheHideCount = IntegerField()
    MembershipLevel = CharField()


class Commented(BaseModel):
    user = ForeignKeyField(User)
    cache = ForeignKeyField(Cache)
    date = DateTimeField()