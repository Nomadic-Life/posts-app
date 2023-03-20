from pydantic import BaseSettings

class Settings(BaseSettings):

    database_hostname: str 
    database_password: str 
    database_port: str 
    database_username: str 
    database_name: str 
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = "/home/joe/python/FASTAPI/app/.env"

settings = Settings()
