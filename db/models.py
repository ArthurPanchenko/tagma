from peewee import *
from db.connect import db


class BaseModel(Model):
    id = AutoField(primary_key=True)

    class Meta:
        database = db
        order_by = 'id'


class Team(BaseModel):
    title = CharField(unique=True)
    color = CharField(null=True)
    text_channel = CharField()
    voice_channel = CharField()

    class Meta:
        db_table = 'teams'


class Player(BaseModel):
    discord = CharField(unique=True)
    nickname = CharField(unique=True)
    dota_id = CharField(unique=True)
    steam_id = CharField(unique=True)
    mmr = IntegerField()
    role = IntegerField()
    team = ForeignKeyField(Team, null=True, on_delete='SET NULL')
    about = TextField()

    class Meta:
        db_table = 'players'
