from app.core.ws.ws_manager import sio
from app.modules.order.service import order_service
from app.dtos.order import OrderDTO
from app.dtos.create_order import CreateOrderDTO
from app.dtos.update_order import UpdateOrderDTO
from app.dtos.get_order import GetOrderDTO


@sio.on("order.create")
async def handle_order_create(sid: str, data: dict) -> None:
    dto = CreateOrderDTO.model_validate(data)
    order = order_service.create(dto.to_service())
    await sio.emit("order.created", OrderDTO.model_validate(order.model_dump()).model_dump(), to=sid)


@sio.on("order.get")
async def handle_order_get(sid: str, data: dict) -> None:
    dto = GetOrderDTO.model_validate(data)
    order = order_service.get_by_id(dto.id)
    if order:
        await sio.emit("order.data", OrderDTO.model_validate(order.model_dump()).model_dump(), to=sid)
    else:
        await sio.emit("order.error", {"message": "Order not found"}, to=sid)


@sio.on("order.list")
async def handle_order_list(sid: str, data: dict) -> None:
    orders = order_service.get_all()
    await sio.emit("order.list", [OrderDTO.model_validate(o.model_dump()).model_dump() for o in orders], to=sid)


@sio.on("order.update")
async def handle_order_update(sid: str, data: dict) -> None:
    order_id = data.get("id", "")
    dto = UpdateOrderDTO.model_validate(data)
    order = order_service.update(order_id, dto.to_service())
    if order:
        await sio.emit("order.updated", OrderDTO.model_validate(order.model_dump()).model_dump(), to=sid)
    else:
        await sio.emit("order.error", {"message": "Order not found"}, to=sid)


@sio.on("order.delete")
async def handle_order_delete(sid: str, data: dict) -> None:
    dto = GetOrderDTO.model_validate(data)
    if order_service.delete(dto.id):
        await sio.emit("order.deleted", {"id": dto.id}, to=sid)
    else:
        await sio.emit("order.error", {"message": "Order not found"}, to=sid)
