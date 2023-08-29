from sqlalchemy import text

from src.configuration.config import sql
from src.model.entity.Rank import Rank
from src.model.entity.User import User


class RankRepository:

    @classmethod
    def getRank(cls, userId) -> Rank:
        rank: Rank = sql.session.query(Rank).from_statement(
            text("SELECT ranks.* "
                 "FROM ranks "
                 "JOIN users "
                 "ON users.rank_id = ranks.rank_id "
                 "WHERE users.user_id = :userId")
        ).params(userId=userId).first()
        return rank

