from pydantic import BaseModel, Field
import os
from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated, Literal

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


class FilterParams(BaseModel):
    price: int = Field(100)
    status: Literal["sold", "not sold"] = "sold"


data = {
    "id": 123
}
user1 = User(**data)


@app.get("/")
async def root():
    return {"name": "Christian"}


@app.get("/items/")
def root_two(item: Annotated[FilterParams, Query()]):
    return {"price": item.price, "status": item.status}


@app.get("/status/{status}")
def root_three(status: Status):
    if status == Status.cancelled:
        return {"status": status, "message": "Order cancelled"}
    elif status == Status.pending:
        return {"status": status, "message": "Order pending"}
    return {"status": status, "message": "Order completed"}


@app.get("/identity/{name}")
def provide_identity(name: Annotated[str | None, Path(min_length=2, max_length=10)], id: int = 10978):
    return {"name": name, "id": id}


@app.get("/name/{name}")
def generate_name(name: Annotated[str, Path(min_length=4, max_length=11)]):
    return {"name": name}


@app.post("/user")
def get_user(user: User):
    return {"id": user.id, "name": user.name}
