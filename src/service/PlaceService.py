from datetime import timedelta, datetime
from typing import Any
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.BanRepository import BanRepository
from src.model.repository.MuteRepository import MuteRepository
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.PlaceRepository import PlaceRepository
from src.model.repository.PurchaseRepository import PurchaseRepository
from src.model.repository.RankRepository import RankRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class PlaceService:

    @classmethod
    def getPlaces(cls):
        places = PlaceRepository.getPlaces()
        return Utils.createSuccessResponse(True, Utils.createList(places))

    @classmethod
    def getPlacesOf(cls, username):
        user = UserRepository.getByUsername(username)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        places = PlaceRepository.getPlacesOf(user.user_id)
        array = []
        for place in places:
            array.append(place[0].toJSON(coords=place[2], level=place[1], rent_cost=Utils.fixNumber(place[0].cost * place[1])))
        return Utils.createSuccessResponse(True, array)

    @classmethod
    def create(cls, request):
        place = PlaceRepository.create(request['name'], request['cost'])
        return Utils.createSuccessResponse(True, "created")

    @classmethod
    def remove(cls, placeId):
        place = PlaceRepository.getPlace(placeId)
        if place is None:
            return Utils.createWrongResponse(False, "place not found", 404), 404
        PlaceRepository.remove(place)
        return Utils.createSuccessResponse(True, "removed")

    @classmethod
    def payRent(cls, request, token):
        user = UserRepository.getByUUID(token)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        place = PlaceRepository.getPlace(request['place_id'])
        if place is None:
            return Utils.createWrongResponse(False, "place not found", 404), 404
        purchase = PurchaseRepository.getPurchase(user.user_id, request['place_id'])
        if purchase is None:
            purchasers = UserRepository.getPurchasersOf(request['place_id'])
            UserRepository.takeMoney(place.cost * 5, user)
            for purchaser in purchasers:
                print(purchaser[0], purchaser[1])
                UserRepository.addMoney(place.cost * purchaser[1], purchaser[0])
                NotificationRepository.create(purchaser[0].user_id, Constants.NOTIFICATIONS['rent'].replace("{username}", user.username).replace("{amount}", str(place.cost * purchaser[1])))
            return Utils.createSuccessResponse(True, {
                'amount': Utils.fixNumber(place.cost * 5),
                'owns': False,
                'payment_required': len(purchasers) > 0,
                'place': place.toJSON()
            })
        if purchase.level < 5:
            purchase = PurchaseRepository.changeLevel(purchase)
            return Utils.createSuccessResponse(True, {
                'level': purchase.level,
                'owns': True
            })
        return Utils.createWrongResponse(False, "up to date", 403), 403

    @classmethod
    def getPlace(cls, uuid, placeId):
        user = UserRepository.getByUUID(uuid)
        if user is None:
            return Utils.createWrongResponse(False, "user not found", 404), 404
        place = PlaceRepository.getPlace(placeId, user.user_id)
        if place is None:
            return Utils.createWrongResponse(False, "place not found", 404), 404
        return Utils.createSuccessResponse(True, place[0].toJSON(coords=place[2]))

    @classmethod
    def getPlaceInCoords(cls, x, z):
        places = PlaceRepository.getPurchasedPlaces()
        print(places)
        for place in places:
            minX = int(place[1].split(",")[0]) - place[0].r
            maxX = int(place[1].split(",")[0]) + place[0].r
            y = int(place[1].split(",")[1])
            minZ = int(place[1].split(",")[2]) - place[0].r
            maxZ = int(place[1].split(",")[2]) + place[0].r
            if float(x) > minX and float(x) < maxX and float(z) > minZ and float(z) < maxZ:
                return Utils.createSuccessResponse(True, place[0].toJSON(owner=place[2].toJSON()))
        return Utils.createWrongResponse(False, "not found", 404), 404
