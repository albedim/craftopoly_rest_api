from flask_jwt_extended import JWTManager

from src.configuration.config import app, sql
from src.controller import UserController, RankController, TicketController, TicketMessageController

# controllers init
app.register_blueprint(TicketController.ticket)
app.register_blueprint(TicketMessageController.ticketMessage)
app.register_blueprint(RankController.rank)
app.register_blueprint(UserController.user)

# modules init
JWTManager(app)


def create_app():
    with app.app_context():
        sql.create_all()
    return app


if __name__ == '__main__':
    create_app().run()