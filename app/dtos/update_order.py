from pydantic import BaseModel
from app.modules.order.types import OrderUpdate


class UpdateOrderDTO(BaseModel):
    status: str | None = None
    item: str | None = None
    quantity: int | None = None

    def to_service(self) -> OrderUpdate:
        return OrderUpdate.model_validate(self.model_dump(exclude_unset=True))
