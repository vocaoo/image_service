from abc import abstractmethod
from typing import Protocol

from src.domain.image.entities import Image
from src.domain.image.value_objects import ImageID, ForeignKey, ImageURL


class ImageRepository(Protocol):
    @abstractmethod
    async def acquire_image_by_id(self, image_id: ImageID) -> Image:
        raise NotImplementedError

    @abstractmethod
    async def add_image(self, image: Image) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_image(self, image_id: ImageID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_existing_images(self, foreign_key: ForeignKey) -> set[ImageURL]:
        raise NotImplementedError
