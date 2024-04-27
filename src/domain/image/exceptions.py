from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainException


@dataclass(eq=False)
class ImageLimitReached(DomainException):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id has reached the image limit'
