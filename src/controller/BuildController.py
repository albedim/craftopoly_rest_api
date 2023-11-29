from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS

from src.service.BuildService import BuildService
from src.service.NotificationService import NotificationService
from src.service.PlaceService import PlaceService
from src.service.UserService import UserService
from src.utils.Utils import Utils

build: Blueprint = Blueprint('BuildController', __name__, url_prefix=Utils.getURL('builds'))


@build.route("/", methods=['POST'])
@cross_origin()
def create():
    return BuildService.create(Utils.getTokenManually(request), request.json)


@build.route("/<placeId>", methods=['DELETE'])
@cross_origin()
def remove(placeId):
    return BuildService.remove(placeId)


@build.route("/", methods=['GET'])
@cross_origin()
def getPlaces():
    return BuildService.getBuilds()
