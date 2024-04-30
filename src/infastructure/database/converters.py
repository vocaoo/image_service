from src.application.image.dto import Image as ImageDTO
from src.domain.image.entities import Image as ImageEntity
from src.domain.image.value_objects import ImageID, ImageURL, ForeignKey
from src.infastructure.database.models import Image as ImageModel


def convert_image_entity_to_db_model(image: ImageEntity) -> ImageModel:
    return ImageModel(
        id=image.id.to_raw(),
        url=image.url.to_raw(),
        foreign_key=image.foreign_key.to_raw(),
    )


def convert_db_model_to_image_entity(image: ImageModel) -> ImageEntity:
    return ImageEntity(
        id=ImageID(image.id),
        url=ImageURL(image.url),
        foreign_key=ForeignKey(image.foreign_key),
    )


def convert_db_model_to_image_dto(image: ImageModel) -> ImageDTO:
    return ImageDTO(
        id=image.id,
        url=image.url,
        foreign_key=image.foreign_key,
    )
