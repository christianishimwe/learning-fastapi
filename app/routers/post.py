from .. import schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..database import conn, cursor
from fastapi import Depends

# get all posts; GET request

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=list[schemas.PostOut])
def get_posts():
    """
    retrieeves all posts of all users
    you don't need to be logged in to see all posts
    """
    cursor.execute(
        """SELECT posts.*, users.email FROM posts JOIN users ON posts.user_id = users.id""")
    all_posts = cursor.fetchall()
    return [{"post": schemas.Post(**post), "owned_by": schemas.UserOut(**post)} for post in all_posts]

# get one post if given an id; GET Request


@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id: int, user_email: str = Depends(oauth2.get_current_user)):
    cursor.execute(
        """SELECT * FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"post": schemas.Post(**post), "owned_by": schemas.UserOut(**post)}

# create a post: POST request


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, user_id=Depends(oauth2.get_current_user)):
    """
    creates a post in the database
    and associeated this post to the user who was logged in and created the post
    input: title and content of the post
    output: the post that was created
    """
    cursor.execute(
        """INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, user_id.id))
    # let's return the post that we just created
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

# update a post; PUT request


@router.put("/{id}")
def update_post(id: int, post: schemas.Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (
            post.title, post.content, id)
    )
    conn.commit()

    updated_post = cursor.fetchone()
    # if there was no such post
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    conn.commit()
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return None
