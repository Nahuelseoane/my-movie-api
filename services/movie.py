from models.movie import MovieModel
from sqlmodel import select

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
