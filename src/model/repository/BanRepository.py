import datetime

from sqlalchemy import text, or_

from src.configuration.config import sql
from src.model.entity.Ban import Ban


class BanRepository:

    @classmethod
    def create(cls, userId, reason, bannedBy, endsOn=None):
        ban = Ban(userId, reason, bannedBy, endsOn)
        sql.session.add(ban)
        sql.session.commit()
        return ban

    @classmethod
    def getCurrentBan(cls, user_id):
        ban = sql.session.query(Ban).filter(Ban.user_id == user_id).filter(or_(Ban.ends_on > datetime.datetime.now(), Ban.ends_on == None)).first()
        return ban

    @classmethod
    def removeBan(cls, currentBan):
        currentBan.ends_on = datetime.datetime.now()
        sql.session.commit()

