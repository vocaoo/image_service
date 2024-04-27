import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.image.interfaces import ImageRepository
from src.domain.image.entities import Image
from src.domain.image.value_objects import ImageID, ImageURL, UserID


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateImage(Command[UUID]):
    id: UUID
    url: ImageURL
    user_id: UserID


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
        user_id = UserID(command.user_id)

        existing_user_images = await self._repository.get_existing_user_images(user_id)
        image = Image.create(image_id, url, user_id, existing_user_images)

        await self._repository.add_image(image)
        await self._mediator.publish(image.pull_events())
        await self._uow.commit()

        logger.info(
            f"User with '{command.user_id}' added new image with '{command.id}' image_id",
            extra={"image": image}
        )

        return command.id
