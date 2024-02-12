from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email:str
    password:str

    model_config = {
        "json_schema_extra":
            {
                "examples":[
                    {
                    "email": "admin@gmail.com",
                    "password": "admin"
                    }
                ]
            }
    }
@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)