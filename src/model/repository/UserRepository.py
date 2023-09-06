from sqlalchemy import text

from src.configuration.config import sql
from src.model.entity.Rank import Rank
from src.model.entity.User import User


class UserRepository:

    @classmethod
    def getByUsername(cls, username) -> User:
        user = sql.session.query(User).filter(User.username == username).first()
        return user

    @classmethod
    def getStaffers(cls) -> User:
        users = sql.session.query(User).from_statement(
            text("SELECT users.* "
                 "FROM users "
                 "JOIN ranks "
                 "ON ranks.rank_id = users.rank_id "
                 "WHERE ranks.staffer = true")
        ).all()
        return users

    @classmethod
    def signin(cls, username, password) -> User:
        user = sql.session.query(User).filter(User.username == username).filter(User.password == password).first()
        return user

    @classmethod
    def create(cls, uuid, username, password):
        user = User(uuid, username, password)
        sql.session.add(user)
        sql.session.commit()
        return user

    @classmethod
    def getByUUID(cls, uuid):
        user = sql.session.query(User).filter(User.uuid == uuid).first()
        return user

    @classmethod
    def getByTelegramUserId(cls, telegramUserId):
        user = sql.session.query(User).filter(User.telegram_user_id != None).filter(User.telegram_user_id == telegramUserId).first()
        return user

    @classmethod
    def getByUserId(cls, userId):
        user = sql.session.query(User).filter(User.user_id == userId).first()
        return user

    @classmethod
    def editRank(cls, user, rankId):
        user.rank_id = rankId
        sql.session.commit()
        return user

    @classmethod
    def changeUsername(cls, user, username):
        user.username = username
        sql.session.commit()

    @classmethod
    def generateTelegramCode(cls, user, code):
        user.telegram_code = code
        sql.session.commit()

    @classmethod
    def getByTelegramCode(cls, code):
        user = sql.session.query(User).filter(User.telegram_code == code).first()
        return user

    @classmethod
    def createTelegramUserId(cls, user, telegramUserId):
        user.telegram_user_id = telegramUserId
        sql.session.commit()

    @classmethod
    def removeTelegramUserId(cls, user):
        user.telegram_user_id = None
        sql.session.commit()