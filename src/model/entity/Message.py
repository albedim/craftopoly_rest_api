import datetime
from src.configuration.config import sql


class Message(sql.Model):
    __tablename__ = 'messages'
    message_id: int = sql.Column(sql.Integer, primary_key=True)
    ticket_id: int = sql.Column(sql.Integer, nullable=False)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    content: str = sql.Column(sql.String(240), nullable=False)
    created_on: datetime.date = sql.Column(sql.Date, nullable=True)

    def __init__(self, ticketId, userId, content):
        self.ticketId = ticketId
        self.userId = userId
        self.content = content
        self.created_on = datetime.date.today()

    def toJSON(self, **kvargs):
        obj = {
            'message_id': self.message_id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_on': str(self.created_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj