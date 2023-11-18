from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS
from src.service.UserService import UserService
from src.utils.Utils import Utils

user: Blueprint = Blueprint('UserController', __name__, url_prefix=Utils.getURL('users'))


@user.route("/<username>/rank", methods=['GET'])
@cross_origin()
def getRank(username):
    return UserService.getRank(username)


@user.route("/<username>", methods=['GET'])
@cross_origin()
def getUser(username):
    return UserService.getUser(username)


@user.route("/discord/<discordUserId>", methods=['GET'])
@cross_origin()
def getUserByDiscordId(discordUserId):
    return UserService.getUserByDiscordId(discordUserId)


@user.route("/telegram/<telegramUserId>", methods=['GET'])
@cross_origin()
def getUserByTelegramId(telegramUserId):
    return UserService.getUserByTelegramId(telegramUserId)


@user.route("/<username>/exists", methods=['GET'])
@cross_origin()
def exists(username):
    return UserService.exists(username)


@user.route("/online", methods=['POST'])
@cross_origin()
def setOnline():
    return UserService.setOnline(Utils.getTokenManually(request))


@user.route("/offline", methods=['POST'])
@cross_origin()
def setOffline():
    return UserService.setOffline(Utils.getTokenManually(request))


@user.route("/create", methods=['POST'])
@cross_origin()
def create():
    return UserService.create(request.json)


@user.route("/staffers", methods=['GET'])
@cross_origin()
def getStaffers():
    return UserService.getStaffers()


@user.route("/staffers/chat", methods=['GET'])
@cross_origin()
def getStaffersChat():
    return UserService.getStafferChat(Utils.getTokenManually(request))


@user.route("/signin", methods=['POST'])
@cross_origin()
def signin():
    return UserService.signin(request.json)


@user.route("/dices/add", methods=['POST'])
@cross_origin()
def addDices():
    return UserService.addDices(request.json, Utils.getTokenManually(request))


@user.route("/bank/rob", methods=['POST'])
@cross_origin()
def robFromBank():
    return UserService.robFromBank(Utils.getTokenManually(request), request.json)


@user.route("/bank/prepare", methods=['POST'])
@cross_origin()
def prepareBank():
    return UserService.prepareBank(Utils.getTokenManually(request))


@user.route("/<username>/bank/rewards", methods=['GET'])
@cross_origin()
def getRewards(username):
    return UserService.getRewards(username)


@user.route("/money/take", methods=['POST'])
@cross_origin()
def takeMoney():
    return UserService.takeMoney(Utils.getTokenManually(request))


@user.route("/money/add", methods=['POST'])
@cross_origin()
def addMoney():
    return UserService.addMoney(Utils.getTokenManually(request))


@user.route("/dices/use", methods=['PUT'])
@cross_origin()
def useDice():
    return UserService.useDice(request.json, Utils.getTokenManually(request))


@user.route("/sync", methods=['POST'])
@cross_origin()
def sync():
    return UserService.sync(Utils.getTokenManually(request), request.json)


@user.route("/discord/connect", methods=['PUT'])
@cross_origin()
def addDiscordId():
    return UserService.createDiscordUserId(request.json)


@user.route("/discord/disconnect", methods=['PUT'])
@cross_origin()
def removeDiscordId():
    return UserService.removeDiscordUserId(Utils.getTokenManually(request))


@user.route("/discord/generate", methods=['PUT'])
@cross_origin()
def generateDiscordCode():
    return UserService.generateDiscordCode(Utils.getTokenManually(request))


@user.route("/telegram/connect", methods=['PUT'])
@cross_origin()
def addTelegramId():
    return UserService.createTelegramUserId(request.json)


@user.route("/telegram/disconnect", methods=['PUT'])
@cross_origin()
def removeTelegramId():
    return UserService.removeTelegramUserId(Utils.getTokenManually(request))


@user.route("/telegram/generate", methods=['PUT'])
@cross_origin()
def generateCode():
    return UserService.generateTelegramCode(Utils.getTokenManually(request))


@user.route("/staffers/command/<command>", methods=['GET'])
@cross_origin()
def canCommand(command):
    return UserService.canCommand(command, Utils.getTokenManually(request))


@user.route("/rank/upgrade", methods=['PUT'])
@cross_origin()
def upgradeRank():
    return UserService.upgradeRank(Utils.getTokenManually(request), request.json)


@user.route("/rank/downgrade", methods=['PUT'])
@cross_origin()
def downgradeRank():
    return UserService.downgradeRank(Utils.getTokenManually(request), request.json)
