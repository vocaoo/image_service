from abc import ABC

from didiator import EventHandler as DEventHandler

from src.domain.common.events.event import Event


class EventHandler[E: Event](DEventHandler[E], ABC):
    pass
