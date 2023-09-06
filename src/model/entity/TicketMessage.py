import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class TicketMessage(sql.Model):
    __tablename__ = 'ticket_messages'
    message_id: int = sql.Column(sql.Integer, primary_key=True)
    ticket_id: int = sql.Column(sql.Integer, nullable=False)
    user_id: int = sql.Column(sql.Integer, nullable=False)
    content: str = sql.Column(sql.String(240), nullable=False)
    created_on: datetime.datetime = sql.Column(sql.DateTime, nullable=True)

    def __init__(self, ticketId, userId, content):
        self.ticket_id = ticketId
        self.user_id = userId
        self.content = content
        self.created_on = Utils.datetime()

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
