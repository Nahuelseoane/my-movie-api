from pydantic import BaseModel

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