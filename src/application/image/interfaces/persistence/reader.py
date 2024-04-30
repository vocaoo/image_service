from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.image.dto import Image, Images
from src.application.common.pagination import Pagination


class ImageReader(Protocol):
    @abstractmethod
    async def get_image_by_id(self, image_id: UUID) -> Image:
        raise NotImplementedError

    @abstractmethod
    async def get_images_by_foreign_key(self, foreign_key: UUID, pagination: Pagination) -> Images:
        raise NotImplementedError
