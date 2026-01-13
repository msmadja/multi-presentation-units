from fastapi import APIRouter, HTTPException
from app.modules.order.service import order_service
from app.dtos.order import OrderDTO
from app.dtos.create_order import CreateOrderDTO
from app.dtos.update_order import UpdateOrderDTO

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/")
async def get_orders() -> list[OrderDTO]:
    orders = order_service.get_all()
    return [OrderDTO.model_validate(o.model_dump()) for o in orders]


@router.post("/")
async def create_order(dto: CreateOrderDTO) -> OrderDTO:
    order = order_service.create(dto.to_service())
    return OrderDTO.model_validate(order.model_dump())


@router.get("/{order_id}")
async def get_order(order_id: str) -> OrderDTO:
    order = order_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderDTO.model_validate(order.model_dump())


@router.put("/{order_id}")
async def update_order(order_id: str, dto: UpdateOrderDTO) -> OrderDTO:
    order = order_service.update(order_id, dto.to_service())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderDTO.model_validate(order.model_dump())


@router.delete("/{order_id}")
async def delete_order(order_id: str) -> dict[str, str]:
    if not order_service.delete(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
