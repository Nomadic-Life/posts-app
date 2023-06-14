from fastapi import FastAPI 
# req for CORS 
from fastapi.middleware.cors import CORSMiddleware
from .pkg import models
from .pkg.database import engine
from .routers import post, user, auth, vote
from .config import settings 

# don't need this since we'regit using alembic. Could leave it and it wouldn't break anything it would just uild missing talbles upon starting
 # models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# list of domains that can talk to our API. You could also use CORS middle to restrict which methods and headers are allowed 
origin = ["*"]
# If you want your API to be used outside of your domain you need to implement CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the jungle we got fun and games!"}
