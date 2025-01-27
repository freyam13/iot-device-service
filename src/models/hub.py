from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Hub(BaseModel):
    id: str
    name: str
    dwelling_id: Optional[str] = None
    paired_device_ids: List[str] = []

    model_config = ConfigDict(from_attributes=True)
