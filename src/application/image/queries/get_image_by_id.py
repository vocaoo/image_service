import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.query import Query, QueryHandler
from src.application.image.dto import Image
from src.application.image.interfaces import ImageReader


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetImageByID(Query[Image]):
    id: UUID


class GetImageByIDHandler(QueryHandler[GetImageByID, Image]):
    def __init__(self, reader: ImageReader) -> None:
        self._reader = reader

    async def __call__(self, command: GetImageByID) -> Image:
        image = self._reader.get_image_by_id(command.id)
        logger.debug("Get image by id", extra={"image_id": command.id, "image": image})
        return image
