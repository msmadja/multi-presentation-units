from pydantic import BaseModel


class OrderDTO(BaseModel):
    id: str
    status: str
    item: str
    quantity: int
