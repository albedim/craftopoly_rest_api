from src.model.repository.RankRepository import RankRepository
from src.model.repository.TicketMessageRepository import TicketMessageRepository
from src.model.repository.TicketRepository import TicketRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class TicketMessageService:

    @classmethod
    def create(cls, platform, token, request):
        ticket = TicketRepository.getTicket(request['ticket_id'])
        if ticket is None:
            return Utils.createWrongResponse(
                False,
                Constants.NOT_FOUND,
                404
            ), 404
        else:
            if not ticket.open:
                return Utils.createWrongResponse(
                    False,
                    Constants.NOT_ENOUGH_PERMISSIONS,
                    422
                ), 422
            else:
                if platform == 'mcserver':
                    user = UserRepository.getByUUID(token)
                    if user is None:
                        return Utils.createWrongResponse(
                            False,
                            Constants.NOT_FOUND,
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
                                Constants.NOT_ENOUGH_PERMISSIONS,
                                403
                            ), 403
                elif platform == 'website':
                    user = Utils.decodeToken(token)['sub']
                    if user is None:
                        return Utils.createWrongResponse(
                            False,
                            Constants.NOT_FOUND,
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
                                Constants.NOT_ENOUGH_PERMISSIONS,
                                403
                            ), 403
