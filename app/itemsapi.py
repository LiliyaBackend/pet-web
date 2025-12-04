from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import item_service
from app.restapi.schemas import MathItemSchema
from app.service.item_service import ItemService

router = APIRouter()

@router.get("/api/v1/items", response_model=list[MathItemSchema],
            summary="This operation returns all items in shop",
            responses={
                200: {"description": "JSON list of all items in shop"}
            })
def get_all(item_service: Annotated[ItemService, Depends(item_service)]):
    return list(MathItemSchema(**object_to_dict(item)) for item in item_service.get_formulas())

@router.get("/api/v1/items/{id}", response_model=MathItemSchema,
            summary="This operation returns selected item by it's ID",
            responses={
                200: {"description": "JSON representation of item"},
                404: {"description": "Item not found"},
            })
def get_one_item(id, item_service: Annotated[ItemService, Depends(item_service)]):
    item = item_service.get_formula_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return MathItemSchema(**object_to_dict(item))

def object_to_dict(src):
    """Transforms object to dictionary without internal fields which are started by _.

    :param src: object
    :return: dictionary from all non-internal fields
    """

    return {k: v for k, v in src.__dict__.items() if k[0] != '_'}