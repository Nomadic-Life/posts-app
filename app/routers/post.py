from typing import List, Optional
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
from pkg import database, models, oauth2, schemas


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    # to perfom the following SQL query: SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id
    # results = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(
    #    models.Posts.id).all()

    posts = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    results = [{ "Post": Post, "votes": votes } for Post, votes in posts ]

    # if you want posts to be private. if you only want to return posts the user owns
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    
       
    return results


# title str, content str
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # using the paramitizeposts = db.query(models.Posts).all()d %s ensures no strange SQL input, injections 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post= models.Posts(title=post.title, content=post.content, published=post.published)
    # replaced above where you list out all reuired fileds. As entries in you db models increse this becomes unfeasible using **post.dict() gives 
    # all fileds from pydantic models
    new_post = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post 


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)): 
   
    # (str(id),) extra comma at the end helps avoid some issues not sure exactly why
    #    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    #    post = cursor.fetchone()

    # Doing it this way will have it continue search through all rows even after the id is found using .all(). use firts(). We know once it's found no need to contiue to search 
    #replaced by below query with join in order to add vote count for a particular post
    #post = db.query(models.Posts).filter(models.Posts.id == id).first()
    
    post = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(
        models.Posts.id).filter(models.Posts.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    p , v = post
    
    results = { "Post": p, "votes": v }
    
    
    ''' used if you want to make posts private
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    '''
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    # cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
   
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

#    cursor.execute(""" UPDATE posts SET title =%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
#   updated_post = cursor.fetchone()
#   conn.commit() 
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)             
    
    db.commit()   

    return post_query.first()