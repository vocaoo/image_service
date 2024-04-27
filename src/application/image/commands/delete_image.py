import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.image.interfaces import ImageRepository
from src.domain.image.value_objects import ImageID


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteImage(Command[None]):
    id: UUID


class DeleteImageHandler(CommandHandler[DeleteImage, None]):
    def __init__(
        self,
        repository: ImageRepository,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: DeleteImage) -> UUID:
        image_id = ImageID(command.id)

        image = await self._repository.acquire_image_by_id(image_id)
        image.delete()

        await self._repository.delete_image(image_id)
        await self._mediator.publish(image.pull_events())
        await self._uow.commit()

        logger.info(
            f"Image with '{command.id}' image_id is deleted",
            extra={"image": image}
        )

        return command.id
