import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.image.interfaces import ImageRepository
from src.domain.image.entities import Image
from src.domain.image.value_objects import ImageID, ImageURL, ForeignKey


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateImage(Command[UUID]):
    id: UUID
    url: str
    foreign_key: UUID


class CreateImageHandler(CommandHandler[CreateImage, UUID]):
    def __init__(
        self,
        repository: ImageRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateImage) -> UUID:
        image_id = ImageID(command.id)
        url = ImageURL(command.url)
        foreign_key = ForeignKey(command.foreign_key)

        existing_images = await self._repository.get_existing_images(foreign_key)
        image = Image.create(image_id, url, foreign_key, existing_images)

        await self._repository.add_image(image)
        await self._mediator.publish(image.pull_events())
        await self._uow.commit()

        logger.info(
            f"Added new image with '{command.id}' image_id",
            extra={"image": image}
        )

        return command.id
