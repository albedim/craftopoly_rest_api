import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Purchase(sql.Model):
    __tablename__ = 'purchases'
    user_id: int = sql.Column(sql.Integer, sql.ForeignKey("users.user_id"), primary_key=True)
    place_id: int = sql.Column(sql.Integer, sql.ForeignKey("places.place_id"), primary_key=True)
    level: int = sql.Column(sql.Integer, nullable=False)

    def __init__(self, userId, placeId):
        self.user_id = userId
        self.place_id = placeId
        self.level = 1

    def toJSON(self, **kvargs):
        obj = {
            'ban_id': self.ban_id,
            'user_id': self.user_id,
            'reason': self.reason,
            'banned_by': self.banned_by,
            'banned_on': str(self.banned_on),
            'ends_on': str(self.ends_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj