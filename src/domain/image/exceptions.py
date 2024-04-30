from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainException


@dataclass(eq=False)
class ImageLimitReached(DomainException):
    foreign_key: UUID

    @property
    def title(self) -> str:
        return f'The foreign key "{self.foreign_key}" has reached the image limit'
