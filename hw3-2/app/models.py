from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(256), nullable=False, unique=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    


class Post(Base): 
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title= Column(String(100), nullable=False)
    description = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    