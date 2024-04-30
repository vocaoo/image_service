from dataclasses import dataclass
from typing import Self

from src.domain.common.entities import AggregateRoot
from src.domain.image.events import ImageCreated, ImageDeleted
from src.domain.image.exceptions import ImageLimitReached
from src.domain.image.value_objects import ImageURL, ImageID, ForeignKey


IMAGE_LIMIT = 10


@dataclass
class Image(AggregateRoot):
    id: ImageID
    url: ImageURL
    foreign_key: ForeignKey

    @classmethod
    def create(
        cls, image_id: ImageID,
        url: ImageURL,
        foreign_key: ForeignKey,
        existing_images: set[ImageURL],
    ) -> Self:
        if len(existing_images) > IMAGE_LIMIT:
            raise ImageLimitReached(foreign_key.to_raw())

        image = cls(image_id, url, foreign_key)
        image.record_event(
            ImageCreated(
                id=image_id.to_raw(),
                url=url.to_raw(),
                foreign_key=foreign_key.to_raw(),
            )
        )
        return image

    def delete(self) -> None:
        self.record_event(
            ImageDeleted(
                id=self.id.to_raw(),
                url=self.url.to_raw(),
                foreign_key=self.foreign_key.to_raw()
            )
        )
