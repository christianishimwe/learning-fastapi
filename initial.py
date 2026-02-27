from pydantic import BaseModel
import os
from fastapi import FastAPI, Query
from enum import Enum
from typing import Annotated

app = FastAPI()


class User(BaseModel):
    id: int
    name: str = "John Doe"


class Product(BaseModel):
    id: int
    name: str
    price: float


class Market(BaseModel):
    name: str
    users: list[User]
    location: str
    products: list[Product]


class Status(str, Enum):
    cancelled = "cancelled"
    pending = "pending"
    completed = "completed"


data = {
    "id": 123
}
user1 = User(**data)


@app.get("/")
async def root():
    return {"name": "Christian"}


@app.get("/items/{id}")
def root_two(id: int):
    return User(id=id, name="John Doe")


@app.get("/status/{status}")
def root_three(status: Status):
    if status == Status.cancelled:
        return {"status": status, "message": "Order cancelled"}
    elif status == Status.pending:
        return {"status": status, "message": "Order pending"}
    return {"status": status, "message": "Order completed"}


@app.get("/identity/{name}")
def provide_identity(name: Annotated[str | None, Query(min_length=2, max_length=10)] = "Christian", id: int = 10978):
    return {"name": name, "id": id}


@app.post("/user")
def get_user(user: User):
    return {"id": user.id, "name": user.name}
