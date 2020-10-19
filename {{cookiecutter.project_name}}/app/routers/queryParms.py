from fastapi import APIRouter,Query
from typing import Optional

router = APIRouter()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/query")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@router.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@router.get("/model2/{model_name}")
async def get_model(q: str = Query("default", min_length=3)):
    return {"model_name": q, "message": "LeCNN all the images"}