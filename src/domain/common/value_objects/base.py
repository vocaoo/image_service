from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        pass


@dataclass(frozen=True)
class ValueObject[V: Any](BaseValueObject, ABC):
    value: V

    def to_raw(self) -> V:
        return self.value
