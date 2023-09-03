import datetime

from sqlalchemy import text

from src.configuration.config import sql
from src.model.entity.Mute import Mute


class MuteRepository:

    @classmethod
    def create(cls, userId, reason, mutedBy, endsOn):
        mute = Mute(userId, reason, mutedBy, endsOn)
        sql.session.add(mute)
        sql.session.commit()
        return mute

    @classmethod
    def getCurrentMute(cls, user_id):
        mute = sql.session.query(Mute).filter(Mute.user_id == user_id).filter(Mute.ends_on > datetime.datetime.now()).first()
        return mute

    @classmethod
    def removeMute(cls, currentMute):
        currentMute.ends_on = datetime.datetime.now()
        sql.session.commit()

