import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Ticket(sql.Model):
    __tablename__ = 'tickets'
    ticket_id: int = sql.Column(sql.Integer, primary_key=True)
    owner_id: int = sql.Column(sql.Integer, nullable=False)
    open: bool = sql.Column(sql.Boolean, nullable=False)
    closed_on: datetime.datetime = sql.Column(sql.DateTime, nullable=True)
    created_on: datetime.datetime = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, ownerId):
        self.owner_id = ownerId
        self.open = True
        self.created_on = Utils.datetime()

    def toJSON(self, **kvargs):
        obj = {
            'ticket_id': self.ticket_id,
            'owner_id': self.owner_id,
            'open': self.open,
            'created_on': str(self.created_on),
            'closed_on': str(self.closed_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj