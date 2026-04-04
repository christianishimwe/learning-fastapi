from .. import schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from ..database import conn, cursor

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    '''
    creates a user in the database
    input: email and password
    '''
    # hash the password - we don't want to store the password in plain text
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    cursor.execute(
        """ INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", (user.email, user.password)
    )
    # obrtain the created user
    create_user = cursor.fetchone()
    conn.commit()
    return create_user


@router.get("/", response_model=schemas.UserOut)
def get_user(current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """
    retrieves the user's information by their id
    input: token of the user
    **output** : the user's information (email)
    """
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (current_user.id,))
    user = cursor.fetchone()
    return user


# this endpoint allows a user to get post they crearted themselves
@router.get("/me/posts", response_model=list[schemas.Post])
def get_user_posts(current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE user_id = %s""",
                   (current_user.id,))
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"posts with user id {id} was not found")
    return posts
