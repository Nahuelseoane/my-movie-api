from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import session
from models.movie import MovieModel
from sqlmodel import select
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=25)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2024)
    rating: float = Field(ge=0.0,le=10.0)
    category: str = Field(max_length=10)
   
    model_config = {
        "json_schema_extra":
            {
                "examples":[
                    {
                    "title": "Mi película",
                    "overview": "Descripción de la película",
                    "year": 2024,
                    "rating": 0.0,
                    "category": "Acción"
                    }
                ]
            }
    }
    
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = session
    statement = select(MovieModel)
    result = db.exec(statement).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = session
    statement = select(MovieModel).where(MovieModel.id == id)
    result = db.exec(statement).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':"No se encontró la pelicula"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session
    statement = select(MovieModel).where(MovieModel.category == category)
    result = db.exec(statement).all()    
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la categoría"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = session
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit() 
    return JSONResponse(status_code=201, content={"message": "Se registró la película"})
    
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session
    statement = select(MovieModel).where(MovieModel.id==id)
    result = db.exec(statement).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No existe ese ID"})
    result.title=movie.title
    result.overview=movie.overview
    result.year=movie.year
    result.rating=movie.rating
    result.category=movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = session
    statement = select(MovieModel).where(MovieModel.id==id)
    result = db.exec(statement).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la película para eliminar"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Se ha ELIMINADO la película"})
            