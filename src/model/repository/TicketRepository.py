from sqlalchemy import text, desc

from src.configuration.config import sql
from src.model.entity.Rank import Rank
from src.model.entity.Ticket import Ticket
from src.model.entity.User import User


class TicketRepository:

    @classmethod
    def getTicket(cls, ticketId) -> Rank:
        ticket: Ticket = sql.session.query(Ticket).filter(Ticket.ticket_id == ticketId).first()
        return ticket

    @classmethod
    def getAllTickets(cls):
        tickets = sql.session.query(Ticket).order_by(desc(Ticket.ticket_id)).all()
        return tickets

    @classmethod
    def getTickets(cls, username):
        tickets = sql.session.query(Ticket).from_statement(
            text("SELECT tickets.* "
                 "FROM tickets "
                 "JOIN users "
                 "ON users.user_id = tickets.owner_id "
                 "WHERE users.username = :username "
                 "ORDER BY tickets.ticket_id DESC")
        ).params(username=username).all()
        return tickets

