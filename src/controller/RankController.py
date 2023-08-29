from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from src.service.RankService import RankService
from src.utils.Utils import Utils


rank: Blueprint = Blueprint('RankController', __name__, url_prefix=Utils.getURL('ranks'))
