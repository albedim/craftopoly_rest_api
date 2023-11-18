import datetime
from src.configuration.config import sql
from src.utils.Constants import Constants


class User(sql.Model):
    __tablename__ = 'users'
    user_id: int = sql.Column(sql.Integer, primary_key=True)
    password: str = sql.Column(sql.String(40), nullable=False)
    username: str = sql.Column(sql.String(40), nullable=False)
    level: int = sql.Column(sql.Integer, nullable=False)
    uuid: str = sql.Column(sql.String(140), nullable=False)
    discord_user_id: str = sql.Column(sql.String(54), nullable=True)
    discord_code: str = sql.Column(sql.String(6), nullable=True)
    telegram_user_id: str = sql.Column(sql.String(54), nullable=True)
    telegram_code: str = sql.Column(sql.String(6), nullable=True)
    created_on: datetime.date = sql.Column(sql.Date, nullable=True)
    rank_id: int = sql.Column(sql.Integer, nullable=False)
    dices: int = sql.Column(sql.Integer, nullable=False)
    final_space: int = sql.Column(sql.Integer, nullable=False)
    last_join: datetime.datetime = sql.Column(sql.DateTime, nullable=False)
    last_quit: datetime.datetime = sql.Column(sql.DateTime, nullable=True)
    money: int = sql.Column(sql.Integer, nullable=False)

    def __init__(self, uuid, username, password):
        self.username = username
        self.uuid = uuid
        self.password = password
        self.rank_id = Constants.PEDINA_RANK_ID
        self.final_space = 0
        self.level = 0
        self.last_join = datetime.datetime.now()
        self.dices = Constants.DEFAULT_DICES
        self.money = Constants.DEFAULT_MONEY
        self.created_on = datetime.date.today()

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'username': self.username,
            'uuid': self.uuid,
            'money': self.money,
            'final_space': self.final_space,
            'last_join': self.last_join,
            'last_quit': self.last_quit,
            'dices': self.dices,
            'level': self.level,
            'created_on': str(self.created_on),
            'rank_id': self.rank_id
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj