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