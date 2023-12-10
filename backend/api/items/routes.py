from typing import Annotated

from fastapi import (APIRouter, status, Form, UploadFile, File, Depends, 
                     HTTPException)
from sqlalchemy.orm import Session

from api.authorization.utils import oauth2_scheme
from dependencies import get_db, get_item_dependency
from schemas import Item, ItemCreate
from services import save_file
from sql import crud


item_router = APIRouter(prefix='/item', tags=['item'])


@item_router.post("/", response_model=Item, 
                  status_code=status.HTTP_201_CREATED)
def create_item(
        title: Annotated[str, Form()], 
        description: Annotated[str, Form()],
        price: Annotated[str, Form()],
        image: Annotated[UploadFile, File()],
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)):
    image_filename = save_file(image.file._file.getbuffer(), image.filename)
    item = ItemCreate(
        title=title,
        description=description,
        image_name=image_filename,
        price=price
    )
    return crud.create_item(db=db, item=item)


@item_router.get("/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 12, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@item_router.get("/{id}", response_model=Item)
def get_item(id:int, item: Item=Depends(get_item_dependency)):
    return item


@item_router.delete("/{id}")
def delete_item(id: int, token: Annotated[str, Depends(oauth2_scheme)], 
                db: Session=Depends(get_db)):
    result = crud.delete_item(db, id)
    if result and result.get('error'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'Item with id:{id} dosnt\'t exists'
        )
    return {
        'message': 'Item has been deleted'
    }
