import datetime
from src.configuration.config import sql


class Mute(sql.Model):
    __tablename__ = 'mutes'
    mute_id: int = sql.Column(sql.Integer, primary_key=True)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    reason: datetime.datetime = sql.Column(sql.String(140), nullable=False)
    muted_by: int = sql.Column(sql.Integer, nullable=False)
    muted_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)
    ends_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, userId, reason, mutedBy, endsOn):
        self.user_id = userId
        self.reason = reason
        self.muted_by = mutedBy
        self.muted_on = datetime.datetime.now()
        self.ends_on = endsOn

    def toJSON(self, **kvargs):
        obj = {
            'mute_id': self.mute_id,
            'user_id': self.user_id,
            'reason': self.reason,
            'muted_by': self.muted_by,
            'muted_on': str(self.muted_on),
            'ends_on': str(self.ends_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj