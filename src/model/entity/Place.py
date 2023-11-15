import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Place(sql.Model):
    __tablename__ = 'places'
    place_id: int = sql.Column(sql.Integer, primary_key=True)
    name: str = sql.Column(sql.String(50), nullable=False)
    cost: int = sql.Column(sql.Integer, nullable=False)
    times: str = sql.Column(sql.String(54), nullable=False)
    coords: str = sql.Column(sql.String(19), nullable=False)

    def __init__(self, times, name, cost, coords):
        self.name = name
        self.cost = cost
        self.coords = coords
        self.times = times

    def toJSON(self, **kvargs):
        obj = {
            'place_id': self.place_id,
            'name': self.name,
            'cost': self.cost,
            'times': self.times,
            'coords': self.coords
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj