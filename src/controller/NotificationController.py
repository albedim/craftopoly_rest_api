from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS

from src.service.NotificationService import NotificationService
from src.service.UserService import UserService
from src.utils.Utils import Utils

notification: Blueprint = Blueprint('NotificationController', __name__, url_prefix=Utils.getURL('notifications'))


@notification.route("/user/<username>", methods=['GET'])
@cross_origin()
def getNotifications(username):
    return NotificationService.getNotifications(username)


@notification.route("/user/<username>/unseen", methods=['GET'])
@cross_origin()
def getUnSeenNotifications(username):
    return NotificationService.getUnseenNotifications(username)
