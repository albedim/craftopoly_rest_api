from sqlalchemy import desc

from src.configuration.config import sql
from src.model.entity.TicketMessage import TicketMessage


class TicketMessageRepository:

    @classmethod
    def getMessages(cls, ticketId):
        messages = sql.session.query(TicketMessage)\
            .filter(TicketMessage.ticket_id == ticketId)\
            .order_by(desc(TicketMessage.message_id)).all()
        return messages

    @classmethod
    def create(cls, ticketId, userId, content):
        message = TicketMessage(ticketId, userId, content)
        sql.session.add(message)
        sql.session.commit()
        return message

