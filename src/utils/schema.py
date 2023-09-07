
SCHEMA = [
    {
        "name": "USER:CREATE",
        "schema": {
            "username": str,
            "password": str
        }
    },
    {
        "name": "BAN:CREATE",
        "schema": {
            "username": str,
            "time": str,
            "reason": str
        }
    },
    {
        "name": "MUTE:CREATE",
        "schema": {
            "username": str,
            "time": str,
            "reason": str
        }
    },
    {
        "name": "TICKET:CREATE",
        "schema": {
            "message": str
        }
    },
    {
        "name": "RANK:UPGRADE",
        "schema": {
            "username": str
        }
    },
    {
        "name": "USER:SIGNIN",
        "schema": {
            "username": str,
            "password": str
        }
    },
    {
        "name": "RANK:DOWNGRADE",
        "schema": {
            "username": str
        }
    },
    {
        "name": "TICKET_MESSAGE:CREATE",
        "schema": {
            "ticket_id": int,
            "message": str
        }
    }
]