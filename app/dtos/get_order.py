from pydantic import BaseModel


class GetOrderDTO(BaseModel):
    id: str
