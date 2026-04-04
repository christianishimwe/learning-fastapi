from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, oauth2
from ..database import conn, cursor
router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteOut)
def add_vote(vote_info: schemas.VoteIn, user_id: int = Depends(oauth2.get_current_user)):
    """
    adds a vote to a post
    associates this vote to the user who was logged in and created the vote
    input: post_id and dir (direction of the vote: 1 for upvote, 0 for downvote)
    output: the vote that was created
    """
    # let's first check if they already voted on this post
    cursor.execute(
        """SELECT * FROM votes WHERE post_id = %s AND user_id = %s""", (
            vote_info.post_id, user_id.id)
    )
    vote = cursor.fetchone()
    if vote and vote_info.dir == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"user {user_id.id} has already voted on post {vote_info.post_id}")

    if not vote and vote_info.dir == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vote does not exist")
    if vote_info.dir == 1:
        cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s, %s) RETURNING *""",
                       (vote_info.post_id, user_id.id))
    else:
        cursor.execute(
            """DELETE FROM votes WHERE post_id = (%s) AND user_id = (%s) RETURNING *""", (vote_info.post_id, user_id.id))
    new_vote = cursor.fetchone()
    conn.commit()
    return new_vote
