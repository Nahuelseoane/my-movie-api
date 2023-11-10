import datetime
from typing import List, Optional

from pydantic import Field, BaseModel

from fastapi import APIRouter
from fastapi import Depends, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder 

# Models
from models.movie import Movie as MovieModel
from config.database import Session

# middlewares
from middlewares.jwt_bearer import JWTBearer

# Services
from services.movie import MovieService

# Schemas
from schemas.movie import Movie

movie_router = APIRouter()


## Get all movies
@movie_router.get('/movies', tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

## Get a movie
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

## Get movies by a category
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Category not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Creates a movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

## Updates a movie
@movie_router.put('/movies/{id}/', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200, content={"message": "The movie has been updated"})

## Deletes a movie
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
            raise HTTPException(status_code=404, detail="Movie was't found")
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content= {"message": "Movie has been deleted"})
