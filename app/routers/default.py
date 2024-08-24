from typing import Union
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Hello-Yu"])
def read_root():
    return {"Hello": "Yu"}

@router.get("/items/{item_id}", tags=["Union"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}