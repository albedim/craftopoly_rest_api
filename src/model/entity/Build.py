import datetime
from src.configuration.config import sql
from src.utils.Utils import Utils


class Build(sql.Model):
    __tablename__ = 'builds'
    build_id: int = sql.Column(sql.Integer, primary_key=True)
    name: str = sql.Column(sql.String(54), nullable=False)
    coords: str = sql.Column(sql.String(11), nullable=False)

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def toJSON(self, **kvargs):
        obj = {
            'build_id': self.build_id,
            'name': self.name,
            'coords': self.coords
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj