from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from .base import TimedBaseModel


class Image(TimedBaseModel):
    __tablename__ = "images"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    url: Mapped[str] = mapped_column(unique=True)
    foreign_key: Mapped[UUID]
