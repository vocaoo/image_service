from dataclasses import dataclass
from uuid import UUID

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class ForeignKey(ValueObject[UUID]):
    value: UUID
