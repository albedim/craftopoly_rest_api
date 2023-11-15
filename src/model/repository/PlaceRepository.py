import datetime

from sqlalchemy import text, or_

from src.configuration.config import sql
from src.model.entity.Ban import Ban
from src.model.entity.Notification import Notification
from src.model.entity.Place import Place
from src.model.entity.Purchase import Purchase
from src.utils.Utils import Utils


class PlaceRepository:

    @classmethod
    def create(cls, coords, times, name, cost):
        place = Place(times, name, cost, coords)
        sql.session.add(place)
        sql.session.commit()
        return place

    @classmethod
    def getPlaces(cls):
        places = sql.session.query(Place).all()
        return places

    @classmethod
    def getPlacesOf(cls, userId):
        places = sql.session.query(Place, Purchase.level).join(Purchase, Purchase.place_id == Place.place_id).filter(Purchase.user_id == userId).all()
        return places

    @classmethod
    def remove(cls, place):
        sql.session.delete(place)
        sql.session.commit()
        return place

    @classmethod
    def getPlace(cls, placeId):
        place = sql.session.query(Place).filter(Place.place_id == placeId).first()
        return place

