import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.query import Query, QueryHandler
from src.application.image.dto import Images
from src.application.image.interfaces import ImageReader
from src.application.common.pagination import Pagination


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetImagesByForeignKey(Query[Images]):
    foreign_key: UUID
    pagination: Pagination


class GetImagesByForeignKeyHandler(QueryHandler[GetImagesByForeignKey, Images]):
    def __init__(self, reader: ImageReader) -> None:
        self._reader = reader

    async def __call__(self, command: GetImagesByForeignKey) -> Images:
        images = await self._reader.get_images_by_foreign_key(command.foreign_key, command.pagination)
        logger.debug("Get images by foreign key", extra={"foreign_key": command.foreign_key, "images": images})
        return images
