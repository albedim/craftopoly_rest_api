from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.BanRepository import BanRepository
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class BanService:

    @classmethod
    def ban(cls, request, token):
        user = UserRepository.getByUUID(token)
        target = UserRepository.getByUsername(request['username'])
        if target is None or user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            userRank = RankRepository.getRankById(user.rank_id)
            if userRank.staffer:
                targetRank = RankRepository.getRankById(target.rank_id)
                if targetRank.rank_id != Constants.ADMIN_RANK_ID:
                    ban = BanRepository.getCurrentBan(target.user_id)
                    if ban is None:
                        if request['time'] == 'perma':
                            createdBan = BanRepository.create(target.user_id, request['reason'], user.user_id)
                            return Utils.createSuccessResponse(
                                True,
                                createdBan.toJSON(
                                    ends_on="perma",
                                    banned_by=user.toJSON()
                                )
                            )
                        else:
                            minutes = Utils.minuteBanConverter(request['time'])
                            if minutes is None:
                                return Utils.createWrongResponse(
                                    False,
                                    Constants.ALREADY_CREATED,
                                    400
                                ), 400
                            else:
                                finalDateTime = Utils.datetime() + timedelta(minutes=minutes)
                                createdBan = BanRepository.create(target.user_id, request['reason'], user.user_id, finalDateTime)
                                return Utils.createSuccessResponse(
                                    True,
                                    createdBan.toJSON(
                                        banned_by=user.toJSON()
                                    )
                                )
                    else:
                        return Utils.createWrongResponse(
                            False,
                            Constants.ALREADY_CREATED,
                            409
                        ), 409
                else:
                    return Utils.createWrongResponse(
                        False,
                        Constants.NOT_ENOUGH_PERMISSIONS,
                        403
                    ), 403
            else:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    403
                ), 403

    @classmethod
    def getBan(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        currentBan = BanRepository.getCurrentBan(user.user_id)
        if currentBan is not None:
            banOwner = UserRepository.getByUserId(currentBan.banned_by)
            return Utils.createSuccessResponse(
                True,
                currentBan.toJSON(
                    ends_on="perma" if currentBan.ends_on is None else str(currentBan.ends_on),
                    banned_by=banOwner.toJSON()
                )
            )
        else:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404

    @classmethod
    def removeBan(cls, uuid, username):
        user = UserRepository.getByUUID(uuid)
        target = UserRepository.getByUsername(username)
        if user is None or target is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_ENOUGH_PERMISSIONS,
                404
            ), 404
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if rank.staffer:
                currentBan = BanRepository.getCurrentBan(target.user_id)
                if currentBan is not None:
                    BanRepository.removeBan(currentBan)
                    return Utils.createSuccessResponse(
                        True,
                        Constants.CREATED
                    )
                else:
                    return Utils.createWrongResponse(
                        False,
                        Constants.NOT_ENOUGH_PERMISSIONS,
                        404
                    ), 404
            else:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    403
                ), 403

