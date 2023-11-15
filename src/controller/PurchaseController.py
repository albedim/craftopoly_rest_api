from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS

from src.service.NotificationService import NotificationService
from src.service.PlaceService import PlaceService
from src.service.PurchaseService import PurchaseService
from src.service.UserService import UserService
from src.utils.Utils import Utils

purchase: Blueprint = Blueprint('PurchaseController', __name__, url_prefix=Utils.getURL('purchases'))


@purchase.route("/", methods=['POST'])
@cross_origin()
def create():
    return PurchaseService.create(Utils.getTokenManually(request), request.json)