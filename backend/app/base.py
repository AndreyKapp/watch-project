from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from .routes import pages_router
from .admin_routes import admin_routes


app_router = APIRouter()
app_router.include_router(pages_router)
app_router.include_router(admin_routes)

templates = Jinja2Templates(directory="templates")
