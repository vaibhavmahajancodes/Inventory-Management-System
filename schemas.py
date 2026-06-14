from pydantic import BaseModel

class Product(BaseModel):
    name: str
    quantity: int
    price: float
    threshold: int

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # admin or user

class UserLogin(BaseModel):
    username: str
    password: str