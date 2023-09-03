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
        user = UserRepository.getByUUID(token)
        target = UserRepository.getByUsername(request['username'])
        if target is None or user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if rank.staffer:
                mute = MuteRepository.getCurrentMute(target.user_id)
                if mute is None:
                    minutes = Utils.minuteConverter(request['time'])
                    finalDateTime = datetime.now() + timedelta(minutes=minutes)
                    createdMute = MuteRepository.create(target.user_id, request['reason'], user.user_id, finalDateTime)
                    return Utils.createSuccessResponse(
                        True,
                        createdMute.toJSON()
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

    @classmethod
    def getMute(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
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
                Constants.NOT_FOUND,
                404
            ), 404

    @classmethod
    def removeMute(cls, uuid, username):
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
            if rank.staffer and user.user_id != target.user_id:
                currentMute = MuteRepository.getCurrentMute(target.user_id)
                if currentMute is not None:
                    MuteRepository.removeMute(currentMute)
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

