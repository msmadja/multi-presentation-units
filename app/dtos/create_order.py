from pydantic import BaseModel
from app.modules.order.types import OrderCreate


class CreateOrderDTO(BaseModel):
    item: str
    quantity: int = 1

    def to_service(self) -> OrderCreate:
        return OrderCreate(item=self.item, quantity=self.quantity)
