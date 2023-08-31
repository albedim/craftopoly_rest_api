from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from src.service.RankService import RankService
from src.service.MessageService import MessageService
from src.utils.Utils import Utils


message: Blueprint = Blueprint('MessageController', __name__, url_prefix=Utils.getURL('messages'))

