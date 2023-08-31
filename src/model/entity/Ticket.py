import datetime
from src.configuration.config import sql


class Ticket(sql.Model):
    __tablename__ = 'tickets'
    ticket_id: int = sql.Column(sql.Integer, primary_key=True)
    owner_id: str = sql.Column(sql.Integer, nullable=False)
    open: bool = sql.Column(sql.String(40), nullable=False)
    created_on: datetime.date = sql.Column(sql.Date, nullable=True)

    def __init__(self, ownerId):
        self.owner_id = ownerId
        self.open = True
        self.created_on = datetime.date.today()

    def toJSON(self, **kvargs):
        obj = {
            'ticket_id': self.ticket_id,
            'owner_id': self.owner_id,
            'open': self.open,
            'created_on': str(self.created_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj