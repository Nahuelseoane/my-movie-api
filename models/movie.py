# from config.database import Base
from typing import Optional
from sqlmodel import SQLModel, Field
# from sqlalchemy import Column, Integer, String, Float

class MovieModel(SQLModel, table=True):
    
    __tablename__ = "movies"
    
    id : Optional[int] = Field(default=None, primary_key=True)
    title : str
    overview : str
    year : int
    rating : float
    category : str