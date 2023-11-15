import datetime

from sqlalchemy import text, or_

from src.configuration.config import sql
from src.model.entity.Ban import Ban
from src.model.entity.Notification import Notification
from src.utils.Utils import Utils


class NotificationRepository:

    @classmethod
    def create(cls, userId, content):
        notification = Notification(userId, content)
        sql.session.add(notification)
        sql.session.commit()
        return notification

    @classmethod
    def getNotifications(cls, user_id):
        notifications = sql.session.query(Notification).filter(Notification.user_id == user_id).all()
        return notifications

    @classmethod
    def remove(cls, notification):
        sql.session.delete(notification)
        sql.session.commit()
        return notification

