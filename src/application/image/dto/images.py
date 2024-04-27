from typing import TypeAlias

from src.application.common.pagination.dto import PaginatedItemsDTO

from .image import Image

Images: TypeAlias = PaginatedItemsDTO[Image]
