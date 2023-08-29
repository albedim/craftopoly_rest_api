from sqlalchemy import text

from src.configuration.config import sql
from src.model.entity.Rank import Rank
from src.model.entity.User import User


class UserRepository:

    @classmethod
    def getByUsername(cls, username) -> Rank:
        user = sql.session.query(User).filter(User.username == username).first()
        return user

