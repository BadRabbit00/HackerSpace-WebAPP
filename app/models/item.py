from pydantic import BaseModel

class Item(BaseModel)::
    """Item schema."""
    id: int
    name: str
    description: str | None = None
    price: float
    is_offer: bool = False