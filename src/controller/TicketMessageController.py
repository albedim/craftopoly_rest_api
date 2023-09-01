from flask import Blueprint, request
from flask_cors import cross_origin
from src.service.TicketMessageService import TicketMessageService
from src.utils.Constants import Constants
from src.utils.Utils import Utils


ticketMessage: Blueprint = Blueprint('MessageController', __name__, url_prefix=Utils.getURL('tickets/messages'))


@ticketMessage.route("/", methods=['POST'])
@cross_origin()
def create():
    platform = request.args.get("platform")

    if platform is None:
        return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

    return TicketMessageService.create(platform, Utils.getTokenManually(request), request.json)