from fastapi import FastAPI, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = '0.0.1'

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email:str
    password:str

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
                    "id": 1,
                    "title": "Mi película",
                    "overview": "Descripción de la película",
                    "year": 2024,
                    "rating": 0.0,
                    "category": "Acción"
                    }
                ]
            }
    }


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':"No se encontró la pelicula"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la categoría"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit() 
    return JSONResponse(status_code=201, content={"message": "Se registró la película"})
    
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No existe ese ID"})
    result.title=movie.title
    result.overview=movie.overview
    result.year=movie.year
    result.rating=movie.rating
    result.category=movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la película"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró la película para eliminar"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Se ha ELIMINADO la película"})
            