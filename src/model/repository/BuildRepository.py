import datetime

from sqlalchemy import text, or_

from src.configuration.config import sql
from src.model.entity.Ban import Ban
from src.model.entity.Build import Build
from src.model.entity.Notification import Notification
from src.model.entity.Place import Place
from src.model.entity.Purchase import Purchase
from src.model.entity.User import User
from src.utils.Utils import Utils


class BuildRepository:

    @classmethod
    def create(cls, name, coords):
        build = Build(name, coords)
        sql.session.add(build)
        sql.session.commit()
        return build

    @classmethod
    def getBuilds(cls):
        builds = sql.session.query(Build).all()
        return builds

    @classmethod
    def getBuild(cls, buildId):
        build = sql.session.query(Build).filter(Build.build_id == buildId).first()
        return build

    @classmethod
    def remove(cls, build):
        sql.session.delete(build)
        sql.session.commit()
        return build
