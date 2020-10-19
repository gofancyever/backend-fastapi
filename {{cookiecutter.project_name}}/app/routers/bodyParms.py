from fastapi import APIRouter,Depends,HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field,EmailStr
from app.schemes import user as schemas
from app.database import get_db
from app.crud import user as crud
router = APIRouter()

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

@router.post("/items/")
async def create_item(item: Item):
    return item

@router.post('/item1', response_model=Item)
async def item1(item: Item):
    return item
@router.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)