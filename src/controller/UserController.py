from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
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


@user.route("/telegram/<telegramUserId>", methods=['GET'])
@cross_origin()
def getUserByTelegramId(telegramUserId):
    return UserService.getUserByTelegramId(telegramUserId)


@user.route("/<username>/exists", methods=['GET'])
@cross_origin()
def exists(username):
    return UserService.exists(username)


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


@user.route("/sync", methods=['POST'])
@cross_origin()
def sync():
    return UserService.sync(Utils.getTokenManually(request), request.json)


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
