import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=80)
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length= 3, max_length=10)

    model_config = {
        "json_schema_extra": {
            "examples":[
                {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2023,
                "rating": 9.8,
                "category": "Acción",
                }
            ]
        }
    }