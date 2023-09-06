import datetime
from datetime import timedelta
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.service.RankService import RankService
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class UserService:

    @classmethod
    def getRank(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            rank = RankRepository.getRankById(5)
            rank.name = rank.name.replace("{level}", "0")
            return Utils.createSuccessResponse(
                True,
                rank.toJSON()
            )

        rank = RankRepository.getRank(user.user_id)
        rank.name = rank.name.replace("{level}", str(user.level))
        return Utils.createSuccessResponse(
            True,
            rank.toJSON()
        )

    @classmethod
    def sync(cls, uuid, request):
        user = UserRepository.getByUUID(uuid)
        if user is not None:
            if user.username != request['username']:
                UserRepository.changeUsername(user, request['username'])
                return Utils.createSuccessResponse(
                    True,
                    Constants.CREATED
                )
            else:
                return Utils.createSuccessResponse(
                    True,
                    Constants.CREATED
                )
        else:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404

    @classmethod
    def canCommand(cls, command, uuid):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404

        rank = RankRepository.getRankById(user.rank_id)
        if command in Constants.COMMANDS:
            return Utils.createSuccessResponse(
                True,
                rank.rank_id <= Constants.COMMANDS[command]
            )
        return Utils.createSuccessResponse(
            True,
            False
        )

    @classmethod
    def exists(cls, username):
        return Utils.createSuccessResponse(
            True,
            UserRepository.getByUsername(username) is not None
        )

    @classmethod
    def getUser(cls, username):
        return Utils.createSuccessResponse(
            True,
            UserRepository.getByUsername(username).toJSON()
        )

    @classmethod
    def getStaffers(cls):
        return Utils.createSuccessResponse(
            True,
            Utils.createList(UserRepository.getStaffers())
        )

    @classmethod
    def getStafferChat(cls, uuid):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_ENOUGH_PERMISSIONS,
                403
            ), 403
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if not rank.staffer:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    403
                ), 403
            else:
                return Utils.createSuccessResponse(
                    True,
                    Utils.createList(UserRepository.getStaffers())
                )

    @classmethod
    def signin(cls, body):
        if not Utils.isValid(body, "USER:SIGNIN"):
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

        user = UserRepository.signin(body['username'], Utils.hash(body['password']))
        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404

        return Utils.createSuccessResponse(True, {
            'token': create_access_token(user.toJSON(), expires_delta=timedelta(weeks=4))
        })

    @classmethod
    def create(cls, body):
        if not Utils.isValid(body, "USER:CREATE"):
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

        exists = UserRepository.getByUsername(body['username']) is not None or \
                 UserRepository.getByUUID(body['uuid']) is not None
        if exists:
            return Utils.createWrongResponse(False, Constants.ALREADY_CREATED, 409), 409

        user = UserRepository.create(body['uuid'], body['username'], Utils.hash(body['password']))
        return Utils.createSuccessResponse(True, user.toJSON())

    @classmethod
    def upgradeRank(cls, uuid, request):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            if user.rank_id == 1 or user.rank_id == 2:
                target = UserRepository.getByUsername(request['username'])
                if target is None:
                    return Utils.createWrongResponse(
                        False,
                        Constants.NOT_FOUND,
                        404
                    ), 404
                else:
                    if user.rank_id == 2:
                        if target.user_id != user.user_id:
                            if target.rank_id > 2:
                                UserRepository.editRank(target, RankService.getUpgradeRank(target))
                                return Utils.createSuccessResponse(
                                    True,
                                    RankRepository.getRankById(target.rank_id).name
                                )
                            else:
                                return Utils.createWrongResponse(
                                    False,
                                    Constants.NOT_ENOUGH_PERMISSIONS + " [auto-upgrade is disabled] ",
                                    403
                                ), 403
                        else:
                            return Utils.createWrongResponse(
                                False,
                                Constants.NOT_ENOUGH_PERMISSIONS + " [auto-upgrade is disabled] ",
                                403
                            ), 403
                    else:
                        if target.rank_id > 1:
                            UserRepository.editRank(target, RankService.getUpgradeRank(target))
                            return Utils.createSuccessResponse(
                                True,
                                RankRepository.getRankById(target.rank_id).name
                            )
                        else:
                            return Utils.createWrongResponse(
                                False,
                                Constants.NOT_ENOUGH_PERMISSIONS + " [auto-upgrade is disabled] ",
                                403
                            ), 403
            else:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    403
                ), 403

    @classmethod
    def downgradeRank(cls, uuid, request):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            if user.rank_id == 1 or user.rank_id == 2:
                target = UserRepository.getByUsername(request['username'])
                if target is None:
                    return Utils.createWrongResponse(
                        False,
                        Constants.NOT_FOUND,
                        404
                    ), 404
                else:
                    if user.rank_id == 2:
                        print(target.rank_id)
                        if target.rank_id > 1 and target.rank_id < 5:
                            UserRepository.editRank(target, RankService.getDowngradeRank(target))
                            return Utils.createSuccessResponse(
                                True,
                                RankRepository.getRankById(target.rank_id).name
                            )
                        else:
                            return Utils.createWrongResponse(
                                False,
                                Constants.NOT_ENOUGH_PERMISSIONS + " [auto-upgradedsfdsggsd is disabled] ",
                                403
                            ), 403
                    else:
                        if target.rank_id >= 1 and target.rank_id < 5:
                            print(target.rank_id)
                            UserRepository.editRank(target, RankService.getDowngradeRank(target))
                            return Utils.createSuccessResponse(
                                True,
                                RankRepository.getRankById(target.rank_id).name
                            )
                        else:
                            return Utils.createWrongResponse(
                                False,
                                Constants.NOT_ENOUGH_PERMISSIONS + " [auto-upgrade is disabled] ",
                                403
                            ), 403
            else:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    403
                ), 403

    @classmethod
    def generateTelegramCode(cls, uuid):
        user = UserRepository.getByUUID(uuid)

        if user is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_ENOUGH_PERMISSIONS,
                404
            ), 404

        if user.telegram_user_id is not None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_ENOUGH_PERMISSIONS,
                409
            ), 409

        code = Utils.createCode(6)
        UserRepository.generateTelegramCode(
            user,
            code
        )

        return Utils.createSuccessResponse(True, code)

    @classmethod
    def createTelegramUserId(cls, request):
        alreadyConnected = UserRepository.getByTelegramUserId(request['telegram_user_id']) is not None

        if alreadyConnected:
            return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 409), 409

        user = UserRepository.getByTelegramCode(request['code'])
        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 404), 404

        UserRepository.createTelegramUserId(user, request['telegram_user_id'])
        return Utils.createSuccessResponse(True, user.username)

    @classmethod
    def removeTelegramUserId(cls, uuid):

        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 404), 404

        connected = user.telegram_user_id is not None

        if not connected:
            return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 404), 404

        UserRepository.removeTelegramUserId(user)
        return Utils.createSuccessResponse(True, Constants.CREATED)
