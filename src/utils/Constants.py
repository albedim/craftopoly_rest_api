import calendar
from datetime import datetime


#
# @author: Alberto Di Maio, albedim <dimaio.albe@gmail.com>
# Created on: 18/04/23
# Created at: 14:35
# Version: 1.0.0
# Description: This is the class for the constants
#

class Constants:
    DAILY_MONEY_BONUS = 5000
    MONEY_PER_TURN = 40
    PERCENTAGES = [20,17,14,10]
    USER_NOT_FOUND: str = "This user was not found"
    NOT_FOUND: str = "Not found"
    NOT_ENOUGH_PERMISSIONS: str = "Not enough permissions"
    CREATED: str = "Created"
    UP_TO_DATE: str = "Up To date"
    NOT_UP_TO_DATE: str = "Not Up To date"
    ALREADY_CREATED = "This resource was already created"
    INVALID_REQUEST: str = "Invalid request"

    HOURS = 2

    COMMANDS = {
        "teleport": 3,
        "vanish": 3,
    }

    NOTIFICATIONS = {
            'bank': '§a{username} §7ha rubato §a{money}€ §7dalla tua banca',
            'rent': '§a{username} §7ha pagato un tuo affitto a §a{amount}€'
    }

    PEDINA_RANK_ID = 5

    CONSOLE_UUID = "SA28S2O346FN2H2HB82BE8"

    ADMIN_RANK_ID = 2
    FOUNDER_RANK_ID = 1

    DEFAULT_MONEY = 15000

    EMAIL = ''
    PASSWORD = ''
    PASSWORD_FORGOTTEN_EMAIL: str = "Hey! \nHere's the link to recover your account: https://cryllet-fe.pages.dev/create_password/{token}"

    PAGE_NOT_FOUND = 'This page was not found. See our documentation'
    PAGE_METHOD_NOT_ALLOWED = 'Method not allowed. See our documentation'
    PAGE_UNKNOWN_ERROR = 'Unknown error'
