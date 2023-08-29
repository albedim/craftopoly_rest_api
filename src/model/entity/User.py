import datetime
from src.configuration.config import sql


class User(sql.Model):
    __tablename__ = 'users'
    user_id: int = sql.Column(sql.Integer, primary_key=True)
    username: str = sql.Column(sql.String(40), nullable=False)
    level: int = sql.Column(sql.Integer, nullable=False)
    created_on: datetime.date = sql.Column(sql.Date, nullable=True)
    rank_id: int = sql.Column(sql.Integer, nullable=False)

    def __init__(self, username):
        self.username = username
        self.rank_id = 1
        self.level = 0
        self.created_on = datetime.date.today()