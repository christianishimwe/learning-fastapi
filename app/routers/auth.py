from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database import conn, cursor
from .. import schemas, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    # we want to find the user with the given email
    cursor.execute("""SELECT * FROM users WHERE email = %s""",
                   (user_credentials.username,))
    user = cursor.fetchone()
    print(user_credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # if the user exists, we want to verify the password
    if not utils.verify_password(user_credentials.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # after this the user is valid
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user['id']})
    # return the token to the user
    return {"access_token": access_token, "token_type": "bearer"}
