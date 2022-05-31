from models import Player, Team
from connect import db


with db:
    db.create_tables([Player, Team])
