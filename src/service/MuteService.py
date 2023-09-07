from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class MuteService:

    @classmethod
    def mute(cls, request, token):

        if not Utils.isValid(request, "MUTE:CREATE"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                400
            ), 400

        user = UserRepository.getByUUID(token)
        target = UserRepository.getByUsername(request['username'])
        if target is None or user is None:
            return Utils.createWrongResponse(
                False,
                "user / target not found",
                404
            ), 404
        else:
            userRank = RankRepository.getRankById(user.rank_id)
            if userRank.staffer:
                targetRank = RankRepository.getRankById(target.rank_id)
                if targetRank.rank_id != Constants.ADMIN_RANK_ID:
                    mute = MuteRepository.getCurrentMute(target.user_id)
                    if mute is None:
                        minutes = Utils.minuteMuteConverter(request['time'])
                        if minutes is None:
                            return Utils.createWrongResponse(
                                False,
                                "time format is wrong. (xs/xm/xh/xd)",
                                400
                            ), 400
                        else:
                            finalDateTime = Utils.datetime() + timedelta(minutes=minutes)
                            createdMute = MuteRepository.create(target.user_id, request['reason'], user.user_id, finalDateTime)
                            return Utils.createSuccessResponse(
                                True,
                                createdMute.toJSON()
                            )
                    else:
                        return Utils.createWrongResponse(
                            False,
                            "user already muted",
                            409
                        ), 409
                else:
                    return Utils.createWrongResponse(
                        False,
                        "you can't mute this user",
                        403
                    ), 403
            else:
                return Utils.createWrongResponse(
                    False,
                    "you are not a staffer",
                    403
                ), 403

    @classmethod
    def getMute(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404
        currentMute = MuteRepository.getCurrentMute(user.user_id)
        if currentMute is not None:
            muteOwner = UserRepository.getByUserId(currentMute.muted_by)
            return Utils.createSuccessResponse(
                True,
                currentMute.toJSON(muted_by=muteOwner.toJSON())
            )
        else:
            return Utils.createWrongResponse(
                False,
                "user is not muted",
                404
            ), 404

    @classmethod
    def removeMute(cls, uuid, username):
        user = UserRepository.getByUUID(uuid)
        target = UserRepository.getByUsername(username)
        if user is None or target is None:
            return Utils.createWrongResponse(
                False,
                "user / target not found",
                404
            ), 404
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if rank.staffer and user.user_id != target.user_id:
                currentMute = MuteRepository.getCurrentMute(target.user_id)
                if currentMute is not None:
                    MuteRepository.removeMute(currentMute)
                    return Utils.createSuccessResponse(
                        True,
                        "user successfully unmuted"
                    )
                else:
                    return Utils.createWrongResponse(
                        False,
                        "user is not muted",
                        404
                    ), 404
            else:
                return Utils.createWrongResponse(
                    False,
                    "you can't mute this user",
                    403
                ), 403

