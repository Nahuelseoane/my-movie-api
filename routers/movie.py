from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from config.database import session
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()
    
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = session
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = session
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':"No se encontró la pelicula"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la categoría"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = session
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se registró la película"})
    
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No existe ese ID"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = session
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la película para eliminar"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message":"Se ha ELIMINADO la película"})
            