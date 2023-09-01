from flask import Blueprint, request
from flask_cors import cross_origin
from src.service.TicketServic import TicketService
from src.utils.Constants import Constants
from src.utils.Utils import Utils


ticket: Blueprint = Blueprint('TicketController', __name__, url_prefix=Utils.getURL('tickets'))


@ticket.route("/", methods=['GET'])
@cross_origin()
def getAll():
    platform = request.args.get("platform")

    if platform is None:
        return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

    return TicketService.getAllTickets(platform, Utils.getTokenManually(request))


@ticket.route("/user/<username>", methods=['GET'])
@cross_origin()
def getOfUser(username):
    return TicketService.getTickets(username)


@ticket.route("/", methods=['POST'])
@cross_origin()
def create():
    platform = request.args.get("platform")

    if platform is None:
        return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

    return TicketService.create(platform, Utils.getTokenManually(request), request.json)


@ticket.route("/<ticketId>", methods=['GET'])
@cross_origin()
def get(ticketId):

    platform = request.args.get("platform")

    if platform is None:
        return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

    return TicketService.getTicket(platform, ticketId, Utils.getTokenManually(request))
