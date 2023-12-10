from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from dependencies import get_db, get_item_dependency
from schemas import Item
from api.authorization.utils import get_current_user
from dependencies.db_session import get_db
from sql import crud


admin_routes = APIRouter(prefix='/admin')

templates = Jinja2Templates(directory="templates")


@admin_routes.get('/', response_class=HTMLResponse)
async def index(request: Request,
                db: Session = Depends(get_db),
                user = Depends(get_current_user)):

    if user is None:
        return templates.TemplateResponse(
                "adminlogin.html",
                {"request": request}
            )

    items = crud.get_items(db)
    items_ser = TypeAdapter(list[Item]).dump_python(items)
    return templates.TemplateResponse(
            "adminpanel.html",
            {"request": request, "items": items_ser}
        )


@admin_routes.get("/item/{id}", response_class=HTMLResponse)
def get_item(request: Request,
             item: Item=Depends(get_item_dependency),
             user = Depends(get_current_user)):

    if user is None:
        return templates.TemplateResponse(
                "adminlogin.html",
                {"request": request}
            )

    return templates.TemplateResponse(
        "adminitem.html",
        {"request": request, "item": item}
    )
