from src.model.repository.TicketMessageRepository import TicketMessageRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Utils import Utils


class TicketMessageService:

    @classmethod
    def create(cls, platform, token, request):
        if platform == 'mcserver':
            user = UserRepository.getByUUID(token)
            message = TicketMessageRepository.create(request['ticket_id'], user.user_id, request['message'])
            return Utils.createSuccessResponse(True, message.toJSON())
        if platform == 'website':
            user = Utils.decodeToken(token)['sub']
            message = TicketMessageRepository.create(request['ticket_id'], user['user_id'], request['message'])
            return Utils.createSuccessResponse(True, message.toJSON())
