from typing import Union
from fastapi import APIRouter
from base import settings, logger

router = APIRouter()

@router.get("/", tags=["Hello-Yu"])
def read_root():
     # Example of using logger
    logger.info("Fetching Hello-Yu")
    return {"Hello": "Yu"}


@router.get("/items/{item_id}", tags=["Union"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
