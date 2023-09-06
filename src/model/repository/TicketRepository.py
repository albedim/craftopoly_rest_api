import datetime

from sqlalchemy import text, desc

from src.configuration.config import sql
from src.model.entity.Ticket import Ticket
from src.utils.Utils import Utils


class TicketRepository:

    @classmethod
    def getTicket(cls, ticketId):
        ticket = sql.session.query(Ticket).filter(Ticket.ticket_id == ticketId).first()
        return ticket

    @classmethod
    def create(cls, userId):
        ticket = Ticket(userId)
        sql.session.add(ticket)
        sql.session.commit()
        return ticket

    @classmethod
    def getOpenTicket(cls, userId):
        ticket = sql.session.query(Ticket).filter(Ticket.owner_id == userId).filter(Ticket.open == True).first()
        return ticket

    @classmethod
    def getAllTickets(cls):
        tickets = sql.session.query(Ticket).filter(Ticket.open == True).order_by(desc(Ticket.ticket_id)).all()
        return tickets

    @classmethod
    def getTickets(cls, username):
        tickets = sql.session.query(Ticket).from_statement(
            text("SELECT tickets.* "
                 "FROM tickets "
                 "JOIN users "
                 "ON users.user_id = tickets.owner_id "
                 "WHERE users.username = :username "
                 "ORDER BY tickets.ticket_id DESC").params(username=username)
        ).all()
        return tickets

    @classmethod
    def closeTicket(cls, ticket):
        ticket.open = False
        sql.session.commit()
        return ticket

    @classmethod
    def addCloseDate(cls, ticket):
        ticket.closed_on = Utils.datetime()
        sql.session.commit()
        return ticket

