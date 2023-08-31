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

