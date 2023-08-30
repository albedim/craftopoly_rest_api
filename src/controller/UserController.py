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


@user.route("/<username>/exists", methods=['GET'])
@cross_origin()
def exists(username):
    return UserService.exists(username)


@user.route("/create", methods=['POST'])
@cross_origin()
def create():
    return UserService.create(request.json)


@user.route("/signin", methods=['POST'])
@cross_origin()
def signin():
    return UserService.signin(request.json)
