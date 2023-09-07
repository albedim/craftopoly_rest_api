from src.model.repository.RankRepository import RankRepository
from src.model.repository.TicketMessageRepository import TicketMessageRepository
from src.model.repository.TicketRepository import TicketRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class TicketMessageService:

    @classmethod
    def create(cls, platform, token, request):

        if not Utils.isValid(request, "TICKET_MESSAGE:CREATE"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                400
            ), 400

        ticket = TicketRepository.getTicket(request['ticket_id'])
        if ticket is None:
            return Utils.createWrongResponse(
                False,
                "ticket not found",
                404
            ), 404
        else:
            if not ticket.open:
                return Utils.createWrongResponse(
                    False,
                    "ticket is closed",
                    422
                ), 422
            else:
                if platform == 'mcserver':
                    user = UserRepository.getByUUID(token)
                    if user is None:
                        return Utils.createWrongResponse(
                            False,
                            "user not found",
                            404
                        ), 404
                    else:
                        rank = RankRepository.getRankById(user.rank_id)
                        if rank.staffer or user.user_id == ticket.owner_id:
                            message = TicketMessageRepository.create(request['ticket_id'], user.user_id, request['message'])
                            return Utils.createSuccessResponse(True, message.toJSON())
                        else:
                            return Utils.createWrongResponse(
                                False,
                                "you are not a staffer / ticket owner",
                                403
                            ), 403
                elif platform == 'website':
                    user = Utils.decodeToken(token)['sub']
                    if user is None:
                        return Utils.createWrongResponse(
                            False,
                            "user not found",
                            404
                        ), 404
                    else:
                        rank = RankRepository.getRankById(user['rank_id'])
                        if rank.staffer or user['user_id'] == ticket.owner_id:
                            message = TicketMessageRepository.create(request['ticket_id'], user['user_id'], request['message'])
                            return Utils.createSuccessResponse(True, message.toJSON())
                        else:
                            return Utils.createWrongResponse(
                                False,
                                "you are not a staffer / ticket owner",
                                403
                            ), 403
                if platform == 'telegram':
                    user = UserRepository.getByTelegramUserId(token)
                    if user is None:
                        return Utils.createWrongResponse(
                            False,
                            "user nor found",
                            404
                        ), 404
                    else:
                        rank = RankRepository.getRankById(user.rank_id)
                        if rank.staffer or user.user_id == ticket.owner_id:
                            message = TicketMessageRepository.create(request['ticket_id'], user.user_id, request['message'])
                            return Utils.createSuccessResponse(True, message.toJSON())
                        else:
                            return Utils.createWrongResponse(
                                False,
                                "you are not a staffer / ticket owner",
                                403
                            ), 403
