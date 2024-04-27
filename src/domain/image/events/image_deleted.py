from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class ImageDeleted(Event):
    id: UUID
    url: str
    user_id: UUID
