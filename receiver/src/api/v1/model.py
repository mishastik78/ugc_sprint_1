from pydantic import BaseModel


class Message(BaseModel):
    film_id: str
    timestamp: int
