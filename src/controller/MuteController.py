from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.MuteService import MuteService
from src.service.UserService import UserService
from src.utils.Utils import Utils

mute: Blueprint = Blueprint('MuteController', __name__, url_prefix=Utils.getURL('mutes'))


@mute.route("/", methods=['POST'])
@cross_origin()
def muteUser():
    return MuteService.mute(request.json, Utils.getTokenManually(request))


@mute.route("/user/<username>", methods=['GET'])
@cross_origin()
def getMute(username):
    return MuteService.getMute(username)


@mute.route("/user/<username>", methods=['PUT'])
@cross_origin()
def removeMute(username):
    return MuteService.removeMute(Utils.getTokenManually(request), username)