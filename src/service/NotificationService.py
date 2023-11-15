from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.BanRepository import BanRepository
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class NotificationService:

    @classmethod
    def getNotifications(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        notifications = NotificationRepository.getNotifications(user.user_id)
        array = []

        for notification in notifications:
            array.append(notification.toJSON())
            NotificationRepository.remove(notification)

        return Utils.createSuccessResponse(True, array)

    @classmethod
    def getUnseenNotifications(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        notifications = NotificationRepository.getNotifications(user.user_id)
        return Utils.createSuccessResponse(True, { 'notifications': len(notifications) })
