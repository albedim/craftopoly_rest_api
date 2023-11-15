from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.BanRepository import BanRepository
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.PlaceRepository import PlaceRepository
from src.model.repository.PurchaseRepository import PurchaseRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class PurchaseService:

    ...

    @classmethod
    def create(cls, token, request):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        place = PlaceRepository.getPlace(request['place_id'])
        if place is None:
            return Utils.createWrongResponse(False, "place not found", 404), 404
        purchase = PurchaseRepository.getPurchase(user.user_id, request['place_id'])
        if purchase is None:
            purchase = PurchaseRepository.create(user.user_id, request['place_id'])
            return Utils.createSuccessResponse(True, "created")
        return Utils.createWrongResponse(False, "already bought", 409), 409