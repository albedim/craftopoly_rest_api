from src.model.entity.Ticket import Ticket
from src.model.repository.TicketMessageRepository import TicketMessageRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.TicketRepository import TicketRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class TicketService:

    @classmethod
    def getTicket(cls, page, platform, ticketId, token):
        ticket: Ticket = TicketRepository.getTicket(ticketId)

        if not page.isnumeric():
            return Utils.createWrongResponse(
                False,
                "page must be integer",
                400
            ), 400
        else:
            page = int(page)

        if ticket is None:
            return Utils.createWrongResponse(
                False,
                "ticket not found",
                404
            ), 404
        else:
            owner = UserRepository.getByUserId(ticket.owner_id)
            user = None

            if platform == "mcserver":
                user = UserRepository.getByUUID(token)
            elif platform == 'website':
                user = Utils.decodeToken(token)['sub']
                user = UserRepository.getByUserId(user['user_id'])
            elif platform == "telegram":
                user = UserRepository.getByTelegramUserId(token)

            if user is None:
                return Utils.createWrongResponse(False, "user not found", 404), 404
            else:
                rank = RankRepository.getRank(user.user_id)
                if rank.staffer or user.user_id == ticket.owner_id:
                    messages = TicketMessageRepository.getMessages(ticketId)

                    res = []
                    counter = page * 10 - 10
                    while counter < page * 10 and counter < len(messages):
                        print(messages[counter].user_id)
                        user = UserRepository.getByUserId(messages[counter].user_id).toJSON()
                        res.append(messages[counter].toJSON(owner=user))
                        counter += 1

                    return Utils.createSuccessResponse(True, ticket.toJSON(owner=owner.toJSON(), messages=res))
                else:
                    return Utils.createWrongResponse(False, "you are not a staffer / ticket owner", 403), 403

    @classmethod
    def getAllTickets(cls, page, platform, token):

        if not page.isnumeric():
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                400
            ), 400
        else:
            page = int(page)

        user = None

        if platform == "mcserver":
            user = UserRepository.getByUUID(token)
        elif platform == 'website':
            user = Utils.decodeToken(token)['sub']
            user = UserRepository.getByUserId(user['user_id'])
        elif platform == "telegram":
            user = UserRepository.getByTelegramUserId(token)

        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        else:
            rank = RankRepository.getRankById(user.rank_id)
            if rank.staffer:
                tickets = TicketRepository.getAllTickets()
                res = []
                counter = page * 10 - 10
                while counter < page * 10 and counter < len(tickets):
                    message = TicketMessageRepository.getMessages(tickets[counter].ticket_id)[-1]
                    messageOwner = UserRepository.getByUserId(message.user_id)
                    ticketOwner = UserRepository.getByUserId(tickets[counter].owner_id).toJSON()
                    res.append(tickets[counter].toJSON(
                        message_owner=messageOwner.username,
                        owner=ticketOwner,
                        message=message.content
                    ))
                    counter += 1
                return Utils.createSuccessResponse(True, res)
            else:
                return Utils.createWrongResponse(False, "you are not a staffer", 403), 403

    @classmethod
    def getTickets(cls, page, username):

        if not page.isnumeric():
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                400
            ), 400
        else:
            page = int(page)

        tickets = TicketRepository.getTickets(username)
        res = []
        counter = page * 10 - 10
        while counter < page * 10 and counter < len(tickets):
            message = TicketMessageRepository.getMessages(tickets[counter].ticket_id)[-1]
            messageOwner = UserRepository.getByUserId(message.user_id)
            ticketOwner = UserRepository.getByUserId(tickets[counter].owner_id).toJSON()
            res.append(tickets[counter].toJSON(
                message_owner=messageOwner.username,
                owner=ticketOwner,
                message=message.content
            ))
            counter += 1

        return Utils.createSuccessResponse(True, res)

    @classmethod
    def hasTicketOpen(cls, userId):
        return TicketRepository.getOpenTicket(userId) is not None

    @classmethod
    def create(cls, platform, token, request):

        if not Utils.isValid(request, "TICKET:CREATE"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                400
            ), 400

        user = None

        if platform == 'mcserver':
            user = UserRepository.getByUUID(token)
        elif platform == 'website':
            user = Utils.decodeToken(token)['sub']
        elif platform == 'telegram':
            user = UserRepository.getByTelegramUserId(token)

        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404
        if cls.hasTicketOpen(user.user_id):
            return Utils.createWrongResponse(False, Constants.ALREADY_CREATED, 409), 409
        ticket = TicketRepository.create(user.user_id)
        message = TicketMessageRepository.create(ticket.ticket_id, user.user_id, request['message'])
        return cls.getTickets("1", user.username)

    @classmethod
    def closeTicket(cls, platform, ticketId, token):
        ticket = TicketRepository.getTicket(ticketId)

        if ticket is None:
            return Utils.createWrongResponse(
                False,
                "ticket not found",
                404
            ), 404

        if not ticket.open:
            return Utils.createWrongResponse(
                False,
                "ticket already closed",
                409
            ), 409

        user = None

        if platform == "mcserver":
            user = UserRepository.getByUUID(token)
        elif platform == 'website':
            user = Utils.decodeToken(token)['sub']
            user = UserRepository.getByUserId(user['user_id'])
        elif platform == "telegram":
            user = UserRepository.getByTelegramUserId(token)

        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404

        rank = RankRepository.getRankById(user.rank_id)
        if rank.staffer or user.user_id == ticket.owner_id:
            TicketRepository.closeTicket(ticket)
            TicketRepository.addCloseDate(ticket)
            return Utils.createSuccessResponse(True, "ticket successfully closed")
        else:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_ENOUGH_PERMISSIONS,
                403
            ), 403
