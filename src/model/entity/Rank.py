import datetime
from src.configuration.config import sql


class Rank(sql.Model):
    __tablename__ = 'ranks'
    rank_id: int = sql.Column(sql.Integer, primary_key=True)
    name: str = sql.Column(sql.String(40), nullable=False)
    staffer: bool = sql.Column(sql.Boolean, nullable=True)

    def __init__(self, name, staffer):
        self.name = name
        self.staffer = staffer

    def toJSON(self, **kvargs):
        obj = {
            'rank_id': self.rank_id,
            'name': self.name,
            'staffer': self.staffer
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj