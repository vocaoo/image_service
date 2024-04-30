from typing import Iterable

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from src.domain.image.entities import Image as ImageEntity
from src.domain.image.value_objects import ForeignKey, ImageURL, ImageID
from src.application.image.interfaces import ImageRepository
from src.infastructure.database.repositories.base import SQLAlchemyRepo
from src.infastructure.database.models import Image
from src.infastructure.database.converters import convert_db_model_to_image_entity, convert_image_entity_to_db_model


class ImageRepositoryImpl(SQLAlchemyRepo, ImageRepository):
    async def acquire_image_by_id(self, image_id: ImageID) -> ImageEntity:
        image: Image | None = await self._session.get(Image, image_id.to_raw(), with_for_update=True)
        if image is None:
            raise  # TODO: Add custom exception here

        return convert_db_model_to_image_entity(image)

    async def add_image(self, image: ImageEntity) -> None:
        db_image = convert_image_entity_to_db_model(image)
        self._session.add(db_image)
        try:
            await self._session.flush((db_image, ))
        except IntegrityError as err:
            raise  # TODO: Add custom exception here

    async def delete_image(self, image_id: ImageID) -> None:
        query = delete(Image).where(Image.id == image_id.to_raw())
        try:
            await self._session.execute(query)
        except IntegrityError as err:
            pass  # TODO: Add custom exception here

    async def get_existing_images(self, foreign_key: ForeignKey) -> set[ImageURL]:
        query = select(Image.url).where(Image.foreign_key == foreign_key.to_raw())
        result: Iterable[str] = self._session.scalars(query)
        existing_images = {ImageURL(url) for url in result}
        return existing_images
