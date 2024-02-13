from pydantic import BaseModel, Field
from typing import Optional

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