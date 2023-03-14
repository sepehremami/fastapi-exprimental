from pathlib import Path
from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import models, oauth2
from database import get_db
from utils import verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


BASE_PATH = Path(__file__).resolve().parent
router = APIRouter(tags=['Authentication'])
path = "/home/zednun/Project/maktab/test/fastapi-exprimental/hw3-2/app/templates"
path_static = "/home/zednun/Project/maktab/test/fastapi-exprimental/hw3-2/app/static"
templates = Jinja2Templates(directory=str(path))

router.mount("/static", StaticFiles(directory=path_static))


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@router.post('/login')
def login_user(request : Request,
                    response:Response, 
                    user_credentials: OAuth2PasswordRequestForm = Depends(), # username # password
                 db:Session = Depends(get_db)):
    print(1)
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    access_tocken = oauth2.create_access_tocken(data={"user_id": user.id})
    response.set_cookie(key="Authorization", value=access_tocken)
    # response = RedirectResponse(url="/protected",status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("profile.html", {"access_tocken": access_tocken, "request": request, "response":response, "token_type": "Bearer", "user": user })

# @router.get('/protected')
# def protected_route(request : Request,
#                     response:Response,
#                     user_credentials: OAuth2PasswordRequestForm = Depends(),
#                     db:Session = Depends(get_db)):
#      return templates.TemplateResponse("profile.html", {"request": request, "response":response, "token_type": "Bearer"})

# sepehr7890
# # password : ]v~ehau5i`qdH_8,*;A$-mKie=E/Wc{'Idk#d,qCZKZ5]pl
#   "username": "sepehr7890",
#   "email": "user@example.com",
#   "created_at": "2023-03-06T17:56:08.008764",
#   "password": "?9](|0<5Mh`V'il N`!DU"
# {
#   "username": "sepehr90",
#   "email": "sepehr90@example.com",
#   "created_at": "2023-03-07T00:34:57.682815+03:30"
# }
	
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNywiZXhwIjoxNjc4MTM4NzY3fQ.breYEtC_vPFn39i-Zp5nnl12S8bKjTKr5tZJ0AEkohY

# {
#   "username": "user1",
#   "email": "user1@example.com",
#   "phone": "string",
#   "password": "6FpnhAV.3{iF+h.mp469I"
# }

# {
#   "access_tocken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2Nzg0NTg1NjB9.UZVtm5bB6aF-cBTycWwaEIupYqxxhAzSEov_IPN2p-c",
#   "tocken_type": "bearer"
# }