from datetime import timedelta
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class RankService:

    @classmethod
    def getDowngradeRank(cls, user):
        return RankRepository.getRankById(user.rank_id + 1).rank_id

    @classmethod
    def getUpgradeRank(cls, user):
        return RankRepository.getRankById(user.rank_id - 1).rank_id

