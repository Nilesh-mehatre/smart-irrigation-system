import jwt
from flask import session,request,jsonify
from models import Users
from __init__ import app,db

class AuthenticationRequired(Exception):
    pass

class InvalidUserEmail(Exception):
    pass

class TokenExpired(Exception):
    pass

class InvalidToken(Exception):
    pass

def checkUser():
    token = session.get("token")
    if not token:
        raise AuthenticationRequired("Authentication required")

    try:
        # Verify and decode the JWT
        payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        email = payload["email"]
        
        # Find the user by email
        user = Users.query.filter_by(email=email).first()
        if not user:
            raise InvalidUserEmail("Invalid user email")
        return user

    except jwt.ExpiredSignatureError:
        raise TokenExpired("Token expired")
    except jwt.InvalidTokenError:
        raise InvalidToken("Invalid token")
