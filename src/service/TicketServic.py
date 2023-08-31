from jwt import decode
from sqlalchemy import text, desc

from src.configuration.config import sql
from src.model.entity.Rank import Rank
from src.model.entity.Ticket import Ticket
from src.model.entity.User import User
from src.model.repository.MessageRepository import MessageRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.TicketRepository import TicketRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class TicketService:

    @classmethod
    def getTicket(cls, platform, ticketId, token):
        ticket: Ticket = TicketRepository.getTicket(ticketId)

        if ticket is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            if platform == "mcserver":
                user = UserRepository.getByUUID(token)
                if user is None:
                    return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404
                else:
                    rank = RankRepository.getRank(user.user_id)
                    if rank.staffer or user.user_id == ticket.owner_id:
                        messages = MessageRepository.getMessages(ticketId)
                        return Utils.createSuccessResponse(
                            True,
                            ticket.toJSON(messages=Utils.createListOfPages(Utils.createList(messages), 5))
                        )
                    else:
                        return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 403), 403
            elif platform == "website":
                user = Utils.decodeToken(token)['sub']
                rank = RankRepository.getRank(user['user_id'])
                if rank.staffer or user['user_id'] == ticket.owner_id:
                    messages = MessageRepository.getMessages(ticketId)
                    return Utils.createSuccessResponse(
                        True,
                        ticket.toJSON(messages=Utils.createListOfPages(Utils.createList(messages), 5))
                    )
                else:
                    return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 403), 403

    @classmethod
    def getAllTickets(cls, platform, token):

        if platform == 'website':
            user = Utils.decodeToken(token)['sub']
            rank = RankRepository.getRankById(user['rank_id'])
            if rank.staffer:
                tickets = TicketRepository.getAllTickets()
                res = []
                for ticket in tickets:
                    message = MessageRepository.getMessages(ticket.ticket_id)[0].content
                    res.append(ticket.toJSON(message=message))
                return Utils.createSuccessResponse(True, Utils.createListOfPages(res, 8))
            else:
                return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 403), 403
        elif platform == 'mcserver':
            user = UserRepository.getByUUID(token)

            if user is None:
                return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404
            else:
                rank = RankRepository.getRankById(user.rank_id)
                if rank.staffer:
                    tickets = TicketRepository.getAllTickets()
                    res = []
                    for ticket in tickets:
                        message = MessageRepository.getMessages(ticket.ticket_id)[0].content
                        res.append(ticket.toJSON(message=message))
                    return Utils.createSuccessResponse(True, Utils.createListOfPages(res, 8))
                else:
                    return Utils.createWrongResponse(False, Constants.NOT_ENOUGH_PERMISSIONS, 403), 403

    @classmethod
    def getTickets(cls, username):
        tickets = TicketRepository.getTickets(username)
        res = []

        for ticket in tickets:
            message = MessageRepository.getMessages(ticket.ticket_id)[0].content
            res.append(ticket.toJSON(message=message))

        return Utils.createSuccessResponse(True, Utils.createListOfPages(res, 8))
