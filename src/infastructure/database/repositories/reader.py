from uuid import UUID
from typing import Iterable

from sqlalchemy import select, func

from src.domain.common.constants import Empty
from src.application.common.pagination import Pagination, SortOrder, PaginationResult
from src.application.image.dto import Images, Image as ImageDTO
from src.application.image.interfaces import ImageReader
from src.infastructure.database.models import Image
from src.infastructure.database.repositories.base import SQLAlchemyRepo
from src.infastructure.database.converters import convert_db_model_to_image_dto
from src.infastructure.database.exception_mapper import exception_mapper


class ImageReaderImpl(SQLAlchemyRepo, ImageReader):
    @exception_mapper
    async def get_images_by_foreign_key(self, foreign_key: UUID, pagination: Pagination) -> Images:
        query = select(Image)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(Image.id.asc())

        if pagination.order is SortOrder.DESC:
            query = query.order_by(Image.id.desc())

        if pagination.offset is not Empty.UNSET:
            query = query.offset(pagination.offset)

        if pagination.limit is not Empty.UNSET:
            query = query.limit(pagination.limit)

        result: Iterable[Image] = await self._session.scalars(query)
        images = [convert_db_model_to_image_dto(image) for image in result]
        images_count = self._get_images_count()
        return Images(data=images, pagination=PaginationResult.from_pagination(pagination, total=images_count))

    @exception_mapper
    async def get_image_by_id(self, image_id: UUID) -> ImageDTO:
        image: Image | None = await self._session.get(Image, image_id)
        if image is None:
            raise # TODO: Add custom exception here

        return convert_db_model_to_image_dto(image)

    async def _get_images_count(self) -> int:
        query = select(func.count(Image.id))

        images_count: int = await self._session.scalar(query)
        return images_count
