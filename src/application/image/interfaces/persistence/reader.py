from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.image.dto import Image, Images


class ImageReader(Protocol):
    @abstractmethod
    async def get_image_by_id(self, image_id: UUID) -> Image:
        raise NotImplementedError

    @abstractmethod
    async def get_images_by_user_id(self, user_id: UUID) -> Images:
        raise NotImplementedError
