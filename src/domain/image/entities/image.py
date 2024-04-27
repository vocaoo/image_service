from dataclasses import dataclass
from typing import Self

from src.domain.common.entities import AggregateRoot
from src.domain.image.events import ImageCreated, ImageDeleted
from src.domain.image.exceptions import ImageLimitReached
from src.domain.image.value_objects import ImageURL, ImageID, UserID


IMAGE_LIMIT = 10


@dataclass
class Image(AggregateRoot):
    id: ImageID
    url: ImageURL
    user_id: UserID

    @classmethod
    def create(
        cls, image_id: ImageID, url: ImageURL, user_id: UserID, existing_images: set[ImageURL]
    ) -> Self:
        if len(existing_images) > IMAGE_LIMIT:
            raise ImageLimitReached(user_id.to_raw())

        image = cls(image_id, url, user_id)
        image.record_event(
            ImageCreated(
                id=image_id.to_raw(),
                url=url.to_raw(),
                user_id=user_id.to_raw(),
            )
        )
        return image

    def delete(self) -> None:
        self.record_event(
            ImageDeleted(
                id=self.id.to_raw(),
                url=self.url.to_raw(),
                user_id=self.user_id.to_raw()
            )
        )
