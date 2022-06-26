from pydantic import BaseModel

class Address(BaseModel):
    location: str
    longitude: int
    latitude: int
