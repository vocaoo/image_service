from abc import abstractmethod
from typing import Protocol

from src.domain.image.entities import Image
from src.domain.image.value_objects import ImageID, UserID, ImageURL


class ImageRepository(Protocol):
    @abstractmethod
    async def add_image(self, image: Image) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_image(self, image_id: ImageID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_existing_user_images(self, user_id: UserID) -> set[ImageURL]:
        raise NotImplementedError
