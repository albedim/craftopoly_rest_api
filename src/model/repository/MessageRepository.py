from sqlalchemy import text, desc

from src.configuration.config import sql
from src.model.entity.Message import Message
from src.model.entity.Rank import Rank
from src.model.entity.Ticket import Ticket
from src.model.entity.User import User


class MessageRepository:

    @classmethod
    def getMessages(cls, ticketId) -> Rank:
        messages = sql.session.query(Message).filter(Message.ticket_id == ticketId).all()
        return messages

