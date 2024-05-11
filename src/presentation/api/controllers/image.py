from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query,status
from didiator import CommandMediator, Mediator, QueryMediator

from src.presentation.api.providers import Stub
from src.presentation.api.controllers.responses import OkResponse
from src.application.image.dto import Image, Images
from src.application.image.commands import CreateImage, DeleteImage
from src.application.image.queries import GetImageByID, GetImagesByForeignKey
from src.application.common.pagination import Pagination, SortOrder


image_router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@image_router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    command: CreateImage,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> OkResponse[Image]:
    image_id = await mediator.send(command)
    image = await mediator.query(GetImageByID(image_id))
    return OkResponse(result=image)


@image_router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete(
    image_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeleteImage(id=image_id))
    return OkResponse()


@image_router.get('/', status_code=status.HTTP_200_OK)
async def get_image_by_id(
    image_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[Image]:
    image = await mediator.query(GetImageByID(id=image_id))
    return OkResponse(result=image)


@image_router.get('/{foreign_key}', status_code=status.HTTP_200_OK)
async def get_images_by_foreign_key(
    foreign_key: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[Images]:
    images = await mediator.query(
        GetImagesByForeignKey(
            foreign_key=foreign_key,
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            )
        )
    )
    return OkResponse(result=images)
