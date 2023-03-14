from pydantic import BaseSettings

class Setting(BaseSettings):
    database_hostname:str
    database_port:str
    database_name:str
    database_password:str
    database_username:str
    secret_key:str
    algorithm:str
    access_tocken_expire_minutes:str
    class Config:
        env_file = ".env"

settings = Setting()

