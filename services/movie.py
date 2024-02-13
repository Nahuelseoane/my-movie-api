from models.movie import MovieModel
from sqlmodel import select
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        statement = select(MovieModel)
        result = self.db.exec(statement).all()
        return result
    
    def get_movie(self, id):
        statement = select(MovieModel).where(MovieModel.id == id)
        result = self.db.exec(statement).first()
        return result
    
    def get_movie_by_category(self, category):
        statement = select(MovieModel).where(MovieModel.category == category)
        result = self.db.exec(statement).all()   
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
        
    def update_movie(self, id, movie:Movie):
        statement = select(MovieModel).where(MovieModel.id==id)
        result = self.db.exec(statement).first()
        result.title=movie.title
        result.overview=movie.overview
        result.year=movie.year
        result.rating=movie.rating
        result.category=movie.category
        self.db.commit()
        return
        
    def delete_movie(self, id):
        statement = select(MovieModel).where(MovieModel.id==id)
        result = self.db.exec(statement).first()
        self.db.delete(result)
        self.db.commit()
        return
