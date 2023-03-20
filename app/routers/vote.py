from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from pkg import schemas, database, models, oauth2



router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)): 
    
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {vote.post_id} does not exist')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    print(vote_query)
    found_vote = vote_query.first()
    #create a vote
    if (vote.direction == 1):
        # check if vote exists
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {vote.post_id}')

        new_vote = models.Vote( post_id = vote.post_id, user_id = current_user.id)        
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else: 

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}