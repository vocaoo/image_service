from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class Image(DTO):
    id: UUID
    url: str
    user_id: UUID
