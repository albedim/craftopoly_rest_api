import datetime
import random
from datetime import timedelta
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.PlaceRepository import PlaceRepository
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
            rank = RankRepository.getRankById(Constants.PEDINA_RANK_ID)
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
                    "username changed"
                )
            else:
                return Utils.createSuccessResponse(
                    True,
                    "up to date"
                )
        else:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404

    @classmethod
    def canCommand(cls, command, uuid):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
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
        user = UserRepository.getByUsername(username)

        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404

        return Utils.createSuccessResponse(
            True,
            user.toJSON(money=Utils.fixNumber(user.money))
        )

    @classmethod
    def getUserByTelegramId(cls, telegramUserId):
        user = UserRepository.getByTelegramUserId(telegramUserId)

        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404

        return Utils.createSuccessResponse(
            True,
            user.toJSON()
        )

    @classmethod
    def getUserByDiscordId(cls, discordUserId):
        user = UserRepository.getByDiscordUserId(discordUserId)

        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404

        return Utils.createSuccessResponse(
            True,
            user.toJSON()
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
                "user not found",
                404
            ), 404
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if not rank.staffer:
                return Utils.createWrongResponse(
                    False,
                    "you are not a staffer",
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
            return Utils.createWrongResponse(False, "user not found", 404), 404

        return Utils.createSuccessResponse(True, {
            'token': create_access_token({'user_id': user.user_id, 'expires_in': 14}, expires_delta=timedelta(days=14)),
            'avatar': "https://mc-heads.net/head/" + user.username
        })

    @classmethod
    def create(cls, body):

        if not Utils.isValid(body, "USER:CREATE"):
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

        exists = UserRepository.getByUsername(body['username']) is not None or \
                 UserRepository.getByUUID(body['uuid']) is not None
        if exists:
            return Utils.createWrongResponse(False, "user already exists", 409), 409

        user = UserRepository.create(body['uuid'], body['username'], Utils.hash(body['password']))
        return Utils.createSuccessResponse(True, user.toJSON())

    @classmethod
    def upgradeRank(cls, uuid, request):

        if not Utils.isValid(request, "RANK:UPGRADE"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                400
            ), 400

        if uuid == Constants.CONSOLE_UUID:
            target = UserRepository.getByUsername(request['username'])
            if target is None:
                return Utils.createWrongResponse(
                    False,
                    "target not found",
                    404
                ), 404
            else:
                if Constants.FOUNDER_RANK_ID < target.rank_id <= Constants.PEDINA_RANK_ID:
                    target = UserRepository.editRank(target, RankService.getUpgradeRank(target))
                    return Utils.createSuccessResponse(
                        True,
                        RankRepository.getRankById(target.rank_id).name
                    )
                return Utils.createWrongResponse(
                    False,
                    "you can't change this rank",
                    403
                ), 403
        else:
            user = UserRepository.getByUUID(uuid)
            if user is None:
                return Utils.createWrongResponse(
                    False,
                    "user not found",
                    404
                ), 404
            else:
                if user.rank_id == Constants.FOUNDER_RANK_ID or user.rank_id == Constants.ADMIN_RANK_ID:
                    target = UserRepository.getByUsername(request['username'])
                    if target is None:
                        return Utils.createWrongResponse(
                            False,
                            "target not found",
                            404
                        ), 404
                    else:
                        if user.rank_id == Constants.ADMIN_RANK_ID:
                            if target.user_id != user.user_id:
                                if target.rank_id > Constants.ADMIN_RANK_ID:
                                    UserRepository.editRank(target, RankService.getUpgradeRank(target))
                                    return Utils.createSuccessResponse(
                                        True,
                                        RankRepository.getRankById(target.rank_id).name
                                    )
                                else:
                                    return Utils.createWrongResponse(
                                        False,
                                        "you can't change this rank",
                                        403
                                    ), 403
                            else:
                                return Utils.createWrongResponse(
                                    False,
                                    "you can't change this rank",
                                    403
                                ), 403
                        else:
                            if target.rank_id > Constants.FOUNDER_RANK_ID:
                                UserRepository.editRank(target, RankService.getUpgradeRank(target))
                                return Utils.createSuccessResponse(
                                    True,
                                    RankRepository.getRankById(target.rank_id).name
                                )
                            else:
                                return Utils.createWrongResponse(
                                    False,
                                    "you can't change this rank",
                                    403
                                ), 403
                else:
                    return Utils.createWrongResponse(
                        False,
                        "you can't change this rank",
                        403
                    ), 403

    @classmethod
    def downgradeRank(cls, uuid, request):

        if not Utils.isValid(request, "RANK:UPGRADE"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                400
            ), 400
        if uuid == Constants.CONSOLE_UUID:
            target = UserRepository.getByUsername(request['username'])
            if target is None:
                return Utils.createWrongResponse(
                    False,
                    "target not found",
                    404
                ), 404
            else:
                if Constants.FOUNDER_RANK_ID <= target.rank_id < Constants.PEDINA_RANK_ID:
                    target = UserRepository.editRank(target, RankService.getDowngradeRank(target))
                    return Utils.createSuccessResponse(
                        True,
                        RankRepository.getRankById(target.rank_id).name
                    )
                return Utils.createWrongResponse(
                    False,
                    "you can't change this rank",
                    403
                ), 403
        else:
            user = UserRepository.getByUUID(uuid)
            if user is None:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_FOUND,
                    404
                ), 404
            else:
                if user.rank_id == Constants.FOUNDER_RANK_ID or user.rank_id == Constants.PEDINA_RANK_ID:
                    target = UserRepository.getByUsername(request['username'])
                    if target is None:
                        return Utils.createWrongResponse(
                            False,
                            "you can't change this rank",
                            404
                        ), 404
                    else:
                        if user.rank_id == Constants.ADMIN_RANK_ID:
                            print(target.rank_id)
                            if Constants.FOUNDER_RANK_ID < target.rank_id < Constants.PEDINA_RANK_ID:
                                UserRepository.editRank(target, RankService.getDowngradeRank(target))
                                return Utils.createSuccessResponse(
                                    True,
                                    RankRepository.getRankById(target.rank_id).name
                                )
                            else:
                                return Utils.createWrongResponse(
                                    False,
                                    "you can't change this rank",
                                    403
                                ), 403
                        else:
                            if Constants.FOUNDER_RANK_ID <= target.rank_id < Constants.PEDINA_RANK_ID:
                                print(target.rank_id)
                                UserRepository.editRank(target, RankService.getDowngradeRank(target))
                                return Utils.createSuccessResponse(
                                    True,
                                    RankRepository.getRankById(target.rank_id).name
                                )
                            else:
                                return Utils.createWrongResponse(
                                    False,
                                    "you can't change this rank",
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
                "user not found",
                404
            ), 404

        if user.telegram_user_id is not None:
            return Utils.createWrongResponse(
                False,
                "user already connected to telegram",
                409
            ), 409

        code = Utils.createCode(6)
        UserRepository.generateTelegramCode(
            user,
            code
        )

        return Utils.createSuccessResponse(True, code)

    @classmethod
    def generateDiscordCode(cls, uuid):
        user = UserRepository.getByUUID(uuid)

        if user is None:
            return Utils.createWrongResponse(
                False,
                "user not found",
                404
            ), 404

        if user.discord_user_id is not None:
            return Utils.createWrongResponse(
                False,
                "user already connected to discord",
                409
            ), 409

        code = Utils.createCode(6)
        UserRepository.generateDiscordCode(
            user,
            code
        )

        return Utils.createSuccessResponse(True, code)

    @classmethod
    def createTelegramUserId(cls, request):

        alreadyConnected = UserRepository.getByTelegramUserId(request['telegram_user_id']) is not None

        if alreadyConnected:
            return Utils.createWrongResponse(False, "user already connected to telegram", 409), 409

        user = UserRepository.getByTelegramCode(request['code'])
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404

        UserRepository.createTelegramUserId(user, request['telegram_user_id'])
        return Utils.createSuccessResponse(True, user.username)

    @classmethod
    def createDiscordUserId(cls, request):

        alreadyConnected = UserRepository.getByDiscordUserId(request['discord_user_id']) is not None

        if alreadyConnected:
            return Utils.createWrongResponse(False, "user already connected to discord", 409), 409

        user = UserRepository.getByDiscordCode(request['code'])
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404

        UserRepository.createDiscordUserId(user, request['discord_user_id'])
        return Utils.createSuccessResponse(True, user.username)

    @classmethod
    def removeTelegramUserId(cls, uuid):

        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404

        connected = user.telegram_user_id is not None

        if not connected:
            return Utils.createWrongResponse(False, "user is not connected to a telegram account", 404), 404

        UserRepository.removeTelegramUserId(user)
        return Utils.createSuccessResponse(True, "disconnected")

    @classmethod
    def removeDiscordUserId(cls, uuid):

        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404

        connected = user.discord_user_id is not None

        if not connected:
            return Utils.createWrongResponse(False, "user is not connected to a discord account", 404), 404

        UserRepository.removeDiscordUserId(user)
        return Utils.createSuccessResponse(True, "disconnected")

    @classmethod
    def useDice(cls, request, token):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        """
        if user.dices < 1:
            return Utils.createWrongResponse(False, "not enough dices", 403), 403
        """
        if user.money - Constants.MONEY_PER_TURN < 0:
            return Utils.createWrongResponse(False, "not enough money", 403), 403
        UserRepository.useDiceWithMoney(request['final_space'], user)
        return Utils.createSuccessResponse(True, {
            'money': Utils.fixNumber(Constants.MONEY_PER_TURN)
        })

    @classmethod
    def addDices(cls, request, token):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        UserRepository.addDices(request['dices'], user)
        return Utils.createSuccessResponse(True, "used")

    @classmethod
    def addMoney(cls, token):
        user = UserRepository.getByUUID(token)
        boughtPlaces = len(PlaceRepository.getPlacesOf(user.user_id))
        money = 2 * (Constants.DEFAULT_MONEY if boughtPlaces == 0 else Constants.DEFAULT_MONEY * boughtPlaces)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        UserRepository.addMoney(money, user)
        return Utils.createSuccessResponse(True, {
            'amount':  Utils.fixNumber(money)
        })

    @classmethod
    def prepareBank(cls, token):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        targets = UserRepository.getUsersExclude(user.user_id)
        newTargets = []
        for target in targets:
            if target.last_quit is not None:
                newTargets.append(target)
        target = random.choice(newTargets)
        return Utils.createSuccessResponse(True, {
            'user': target.toJSON(),
            'max_reward':  Utils.fixNumber(cls.getMoneyPercentages(target.money)[0])
        })

    @classmethod
    def getRewards(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        return Utils.createSuccessResponse(True, {
            'rewards': cls.getMoneyPercentages(user.money)
        })

    @classmethod
    def getMoneyPercentages(cls, money):
        array = []
        for percentage in Constants.PERCENTAGES:
            array.append((percentage * money) / 100)
        return array

    @classmethod
    def takeMoney(cls, token):
        user = UserRepository.getByUUID(token)
        boughtPlaces = len(PlaceRepository.getPlacesOf(user.user_id))
        money = Constants.DEFAULT_MONEY if boughtPlaces == 0 else Constants.DEFAULT_MONEY * boughtPlaces
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        UserRepository.takeMoney(money, user)
        return Utils.createSuccessResponse(True, {
            'amount':  Utils.fixNumber(money)
        })

    @classmethod
    def robFromBank(cls, token, request):
        user = UserRepository.getByUUID(token)
        target = UserRepository.getByUsername(request['target_username'])
        if target is None or user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        UserRepository.addMoney(request['money'], user)
        UserRepository.takeMoney(request['money'], target)
        NotificationRepository.create(
            target.user_id,
            Constants.NOTIFICATIONS['bank']
            .replace("{username}", user.username)
            .replace("{money}", Utils.fixNumber(request['money']))
        )
        return Utils.createSuccessResponse(True, {
            'money': Utils.fixNumber(request['money'])
        })

    @classmethod
    def setOnline(cls, token):
        user: User = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        if user.last_join.date() != datetime.datetime.now().date():
            UserRepository.addMoney(Constants.DAILY_MONEY_BONUS, user)
            UserRepository.setOnline(user)
            return Utils.createSuccessResponse(True, {
                'bonus': True,
                'bonus_value': Constants.DAILY_MONEY_BONUS
            })
        UserRepository.setOnline(user)
        return Utils.createSuccessResponse(True, {
            'bonus': False
        })

    @classmethod
    def setOffline(cls, token):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        UserRepository.setOffline(user)
        return Utils.createSuccessResponse(True, 'set')