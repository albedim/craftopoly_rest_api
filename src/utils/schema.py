
SCHEMA = [
    {
        "name": "USER:CREATE",
        "schema": {
            "username": str,
            "password": str
        }
    },
    {
        "name": "SIGNUP_USER",
        "schema": {
            "complete_name": str,
            "email": str,
            "password": str
        }
    },
    {
        "name": "CHANGE",
        "schema": {
            "email": str,
            "complete_name": str,
            "password": str
        }
    },
    {
        "name": "CHANGE_PASSWORD",
        "schema": {
            "user_id": int,
            "password": str
        }
    }
]