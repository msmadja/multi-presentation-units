import uuid
from app.modules.order.types import Order, OrderCreate, OrderUpdate


class OrderService:
    def __init__(self):
        self._orders: dict[str, Order] = {}

    def create(self, data: OrderCreate) -> Order:
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            status="pending",
            item=data.item,
            quantity=data.quantity
        )
        self._orders[order_id] = order
        return order

    def get_by_id(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def get_all(self) -> list[Order]:
        return list(self._orders.values())

    def update(self, order_id: str, data: OrderUpdate) -> Order | None:
        if order_id not in self._orders:
            return None
        order = self._orders[order_id]
        update_data = data.model_dump(exclude_unset=True)
        updated_order = order.model_copy(update=update_data)
        self._orders[order_id] = updated_order
        return updated_order

    def delete(self, order_id: str) -> bool:
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False


order_service = OrderService()
