from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS

from src.service.NotificationService import NotificationService
from src.service.PlaceService import PlaceService
from src.service.UserService import UserService
from src.utils.Utils import Utils

place: Blueprint = Blueprint('PlaceController', __name__, url_prefix=Utils.getURL('places'))


@place.route("/", methods=['POST'])
@cross_origin()
def create():
    return PlaceService.create(request.json)


@place.route("/<placeId>", methods=['DELETE'])
@cross_origin()
def remove(placeId):
    return PlaceService.remove(placeId)


@place.route("/", methods=['GET'])
@cross_origin()
def getPlaces():
    if request.args.get("x") is None or request.args.get("z") is None:
        return PlaceService.getPlaces()
    return PlaceService.getPlaceInCoords(request.args.get("x"), request.args.get("z"))


@place.route("/<placeId>", methods=['GET'])
@cross_origin()
def getPlace(placeId):
    return PlaceService.getPlace(Utils.getTokenManually(request), placeId)


@place.route("/rent", methods=['POST'])
@cross_origin()
def payRent():
    return PlaceService.payRent(request.json, Utils.getTokenManually(request))


@place.route("/user/<username>", methods=['GET'])
@cross_origin()
def getPlacesOf(username):
    return PlaceService.getPlacesOf(username)
