from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import models
from database import get_db
from sqlalchemy.orm import Session
from config import settings
from schema.user import TockenData
# Secret Key
# Algorithem 
# Expiration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORYTHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_tocken_expire_minutes)
# $2b$12$g3iOlG9P92a1/K1Uxl8jJObg2Wm2dwbNbftDYjqsIlXK4fl08alGy

def create_access_tocken(data:dict): # {"user_id": user.id, "exp": expire}
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)
    return encoded_jwt


def verify_access_tocken(tocken:str, credentials_exception):
    try:
        payload = jwt.decode(tocken, SECRET_KEY, algorithms=[ALGORYTHM])
        id :str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        tocken_data = TockenData(id=id)
    except JWTError:
        raise credentials_exception
    return tocken_data

    

def get_current_user(tocken:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    print(tocken)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"})
    
    get_tocken = verify_access_tocken(tocken, credentials_exception)
    user = db.query(models.User).filter(models.User.id == get_tocken.id).first()
    return user