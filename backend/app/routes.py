from fastapi import (Request, Depends, APIRouter)
from fastapi.templating import Jinja2Templates
from pydantic import TypeAdapter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dependencies import get_db, get_item_dependency
from schemas import Item
from sql import crud


templates = Jinja2Templates(directory="templates")

pages_router = APIRouter()

@pages_router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    items_ser = TypeAdapter(list[Item]).dump_python(items)
    items_slider = items_ser[0:5]
    print(items_ser)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request, 
            "item_list": items_ser,
            "items_slider": items_slider
        }
    )


@pages_router.get("/buy_watch/{id}", response_class=HTMLResponse)
async def order_watch(
        request: Request, item: Item=Depends(get_item_dependency)):
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request, 
            "item": item
        }
    )