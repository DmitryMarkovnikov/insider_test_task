from dataclasses import dataclass, field
from typing import Optional

# from pydantic import Field, BaseModel
from pydantic.config import Enum


class PriceType(Enum):
    AVAILABLE = "available"
    NOT_AVAILABLE = "not_available"


@dataclass
class Pet:
    id: Optional[int] = None
    category: Optional[dict] = field(default_factory=lambda: {"id": 0, "name": "pet_category"})
    name: Optional[str] = field(default_factory=lambda: "pet_name")
    photoUrls: Optional[list] = field(default_factory=lambda: ["dummy_url"])
    tags: Optional[list] = field(default_factory=lambda: [{"id": 0, "name": "pet_tag"}])
    status: Optional[str] = PriceType.AVAILABLE.value

