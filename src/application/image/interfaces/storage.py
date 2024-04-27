from abc import abstractmethod
from typing import Protocol

from src.domain.image.value_objects import ImageURL


class Storage(Protocol):
    @abstractmethod
    async def upload(self, image: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, image_url: ImageURL) -> None:
        raise NotImplementedError
