from typing import List

from pydantic import BaseModel, ConfigDict


class Dwelling(BaseModel):
    id: str
    name: str
    is_occupied: bool = False
    hub_ids: List[str] = []

    model_config = ConfigDict(from_attributes=True)
