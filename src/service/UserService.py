from datetime import timedelta
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class UserService:

    @classmethod
    def getRank(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404
        rank = RankRepository.getRank(user.user_id)
        rank.name = rank.name.replace("{level}", Utils.fixNumber(user.level))
        return Utils.createSuccessResponse(
            True,
            rank.toJSON()
        )

