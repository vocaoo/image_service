from abc import abstractmethod
from typing import Protocol

from src.domain.image.value_objects import UserID, ImageID
from src.application.image.dto import Image, Images


class ImageReader(Protocol):
    @abstractmethod
    async def get_image_by_id(self, image_id: ImageID) -> Image:
        raise NotImplementedError

    @abstractmethod
    async def get_images_by_user_id(self, user_id: UserID) -> Images:
        raise NotImplementedError
