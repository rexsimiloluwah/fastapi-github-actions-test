import jwt
from decouple import config
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET_KEY = config("JWT_SECRET_KEY")


class JwtAuthHelper:
    def __init__(self):
        self.secret = JWT_SECRET_KEY

    def encode_jwt(self, user_id: int) -> str:
        """Encode the JWT token"""
        # Token expires in 30 mins
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_jwt(self, token: str) -> int:
        """Decode the JWT token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]

        except jwt.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=401, detail="Authorization failed, Expired token."
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401, detail="Authorization failed, Invalid token."
            )

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        if not auth:
            raise HTTPException(status_code=401, detail="Not Authenticated.")
        return self.decode_jwt(auth.credentials)
