from fastapi import APIRouter

from .authorization import authorization_router
from .items import item_router

base_router = APIRouter(prefix='/api')

base_router.include_router(item_router)
base_router.include_router(authorization_router)
