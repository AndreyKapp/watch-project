from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from sql.crud import get_object_from_db
from sql.models import Item

from .db_session import get_db


class GetDbObjectDependency:
    def __init__(self, model):
        self.model = model

    def __call__(self, id:int, db:Session = Depends(get_db)):
        obj = get_object_from_db(db, id, self.model)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Object with id:{id} doesn\'t exists'
            )
        return obj


get_item_dependency = GetDbObjectDependency(Item)
