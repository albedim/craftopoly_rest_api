import datetime
from src.configuration.config import sql


class Ban(sql.Model):
    __tablename__ = 'bans'
    ban_id: int = sql.Column(sql.Integer, primary_key=True)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    reason: datetime.datetime = sql.Column(sql.String(140), nullable=False)
    banned_by: int = sql.Column(sql.Integer, nullable=False)
    banned_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)
    ends_on: datetime.datetime = sql.Column(sql.DateTime, nullable=True)

    def __init__(self, userId, reason, mutedBy, endsOn):
        self.user_id = userId
        self.reason = reason
        self.banned_by = mutedBy
        self.banned_on = datetime.datetime.now()
        self.ends_on = endsOn

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