from fastapi import APIRouter

from .routers import users, landscapes

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(landscapes.router)
