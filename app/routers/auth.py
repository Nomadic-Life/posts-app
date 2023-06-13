from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.pkg.database import get_db
from app.pkg import schemas, models, utils, oauth2

router = APIRouter(
    prefix= "/login",
    tags = ['Authentication']

)

@router.post("/", response_model=schemas.Token)
# changed to use fastapi Oauth2PasswordRequestForm to retrieve user creds
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm return username = and pasword =  so user_credentials.email won't work
    #user =   db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user =   db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data = { "user_id" : user.id})
    
    #return a token
    
    return { "access_token" : access_token, "token_type" : "bearer"}