from pathlib import Path
from fastapi import Depends, FastAPI, APIRouter, HTTPException, Request, Response, status
from fastapi.params import Body

import oauth2
from schema.post import Post, PostBase, PostCreate
from schema.user import UserBase, UserOut
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
import models
from fastapi.templating import Jinja2Templates
from schema.user import UserBase, UserUpdate, User 
import utils
import oauth2

router = APIRouter(
    prefix="/posts"   
)


@router.get("/", response_model=List[Post])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: User = Depends(oauth2.get_current_user),
    skip: int = 0,
    limit:int=10, search: Optional[str]=""):

    posts: List[Post] = db.query(models.Post).\
        filter(models.Post.user_id==current_user.id).\
        filter(models.Post.title.contains(search)).\
        limit(limit).offset(skip).all()
    
    return posts


@router.get("/{id}", status_code=200)
def get_post(
        db: Session = Depends(get_db),
        current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.user_id==id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    if post.user_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return {'message': post}


@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_post(new_post: PostCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(oauth2.get_current_user)):
    post_information = new_post.dict()
    post_information.update({"user_id":current_user.id})
    print(post_information)
    post = models.Post(**post_information)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post




@router.delete("/{id}")
def delete_user(id: int, db: Session=Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exit"
        )
    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return {"data":"post deleted",
            "deleted post": post.first()}

@router.put('/posts/{post_id}')
async def update_post(post_update: PostBase, post_id:int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post with id {post_id} does not exit"
        )
    post.update(post_update.dict(), synchronize_session=False)
    db.commit()
    return {'msg':'post updated'}

a= {
    "username": "exampleuser1",
    "email": "exampleuser1@example.com",
    "created_at": "2023-03-10T02:07:32.869125+03:30"
}