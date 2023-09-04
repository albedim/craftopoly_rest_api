from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.BanService import BanService
from src.service.MuteService import MuteService
from src.service.UserService import UserService
from src.utils.Utils import Utils

ban: Blueprint = Blueprint('BanController', __name__, url_prefix=Utils.getURL('bans'))


@ban.route("/", methods=['POST'])
@cross_origin()
def banUser():
    return BanService.ban(request.json, Utils.getTokenManually(request))


@ban.route("/user/<username>", methods=['GET'])
@cross_origin()
def getBan(username):
    return BanService.getBan(username)


@ban.route("/user/<username>", methods=['PUT'])
@cross_origin()
def removeBan(username):
    return BanService.removeBan(Utils.getTokenManually(request), username)