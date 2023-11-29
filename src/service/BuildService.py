from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.BanRepository import BanRepository
from src.model.repository.BuildRepository import BuildRepository
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.PlaceRepository import PlaceRepository
from src.model.repository.PurchaseRepository import PurchaseRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class BuildService:

    @classmethod
    def getBuilds(cls):
        builds = BuildRepository.getBuilds()
        return Utils.createSuccessResponse(True, Utils.createList(builds))

    @classmethod
    def create(cls, uuid, request):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        rank = RankRepository.getRank(user.user_id)
        if not rank.staffer:
            return Utils.createWrongResponse(False, "not enough permissions", 403), 403
        build = BuildRepository.create(request['name'], request['coords'])
        return Utils.createSuccessResponse(True, "created")

    @classmethod
    def remove(cls, buildId):
        build = BuildRepository.getBuild(buildId)
        if build is None:
            return Utils.createWrongResponse(False, "build not found", 404), 404
        BuildRepository.remove(build)
        return Utils.createSuccessResponse(True, "removed")