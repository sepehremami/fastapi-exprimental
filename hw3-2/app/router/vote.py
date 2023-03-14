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
from schema.user import VoteBase
import utils
import oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]   
)



@router.post("/", status_code= status.HTTP_201_CREATED)
async def vote(vote: VoteBase,
                    db: Session = Depends(get_db),
                    current_user = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).\
        filter(models.Vote.post_id == vote.post_id,
                models.Vote.user_id == current_user.id
                )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"current user already voted on this post"
            )
        new_vote = models.Vote(post_id = vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="vote does not exit"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
    return {'message':'successfully removed vote'}



