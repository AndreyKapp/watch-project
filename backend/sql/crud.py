from sqlalchemy.orm import Session

from sql.models import Item, User
from schemas import ItemCreate


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 12):
    return db.query(Item).offset(skip).limit(limit).all()

def delete_item(db: Session, id: int):
    item = db.query(Item).filter(Item.id == id).first()
    if item is None:
        return {
            'error': f'item with id:{id} not found'
        }
    db.delete(item)
    db.commit()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_db_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_object_from_db(db: Session, id: int, model):
    return db.query(model).filter(model.id == id).first()
