import logging

from didiator import CommandDispatcherImpl, EventObserverImpl, Mediator, MediatorImpl, QueryDispatcherImpl
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiMiddleware, DiScopes
from didiator.middlewares.logging import LoggingMiddleware

from src.application.image.commands import (
    CreateImage,
    CreateImageHandler,
    DeleteImage,
    DeleteImageHandler,
)
from src.application.image.queries import (
    GetImageByID, GetImageByIDHandler,
    GetImagesByForeignKey, GetImagesByForeignKeyHandler
)
from src.domain.common.events import Event
from src.infrastructure.dependencies import DiScope
from src.infrastructure.log.event_handler import EventLogger


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(DiScope.REQUEST)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(CreateImage, CreateImageHandler)
    mediator.register_command_handler(DeleteImage, DeleteImageHandler)
    mediator.register_query_handler(GetImageByID, GetImageByIDHandler)
    mediator.register_query_handler(GetImagesByForeignKey, GetImagesByForeignKeyHandler)
    mediator.register_event_handler(Event, EventLogger)
