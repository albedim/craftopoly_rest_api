import datetime

from sqlalchemy import text, or_

from src.configuration.config import sql
from src.model.entity.Ban import Ban
from src.model.entity.Notification import Notification
from src.model.entity.Place import Place
from src.model.entity.Purchase import Purchase
from src.utils.Utils import Utils


class PurchaseRepository:

    @classmethod
    def create(cls, userId, placeId):
        purchase = Purchase(userId, placeId)
        sql.session.add(purchase)
        sql.session.commit()
        return purchase

    @classmethod
    def getPurchase(cls, userId, placeId):
        purchase = sql.session.query(Purchase).filter(Purchase.user_id == userId).filter(Purchase.place_id == placeId).first()
        return purchase

    @classmethod
    def remove(cls, purchase):
        sql.session.delete(purchase)
        sql.session.commit()
        return purchase

    @classmethod
    def changeLevel(cls, purchase):
        purchase.level += 1
        sql.session.commit()
        return purchase

