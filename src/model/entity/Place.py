import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Place(sql.Model):
    __tablename__ = 'places'
    place_id: int = sql.Column(sql.Integer, primary_key=True)
    name: str = sql.Column(sql.String(50), nullable=False)
    cost: int = sql.Column(sql.Integer, nullable=False)

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def toJSON(self, **kvargs):
        obj = {
            'place_id': self.place_id,
            'name': self.name,
            'cost': Utils.fixNumber(self.cost)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj