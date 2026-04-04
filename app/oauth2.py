from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from . import schemas
from .database import conn, cursor
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

# SECREATE KEY
# ALGORITHIM
# expireation time for the token

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    # create the expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # to extract the data
        id: int = payload.get("user_id")
        print(f"id is this {id}")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    # if the token is valid, return the id of the user
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    # fetch the user information
    return schemas.TokenData(id=token.id)
