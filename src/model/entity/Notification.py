import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Notification(sql.Model):
    __tablename__ = 'notifications'
    notification_id: int = sql.Column(sql.Integer, primary_key=True)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    content: str = sql.Column(sql.String(50), nullable=False)
    created_on: int = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, userId, content):
        self.user_id = userId
        self.content = content
        self.created_on = Utils.datetime()

    def toJSON(self, **kvargs):
        obj = {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_on': str(self.created_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj