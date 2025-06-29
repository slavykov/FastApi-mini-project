from pydantic import BaseModel

class Book_Model(BaseModel):
    title: str
    author: str
