from pydantic import BaseModel


class OrderCreate(BaseModel):
    item: str
    quantity: int = 1


class Order(BaseModel):
    id: str
    status: str
    item: str
    quantity: int


class OrderUpdate(BaseModel):
    status: str | None = None
    item: str | None = None
    quantity: int | None = None
