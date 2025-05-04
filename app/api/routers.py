from fastapi import APIRouter
from AI.app.api.endpoints import meal
from app.api.endpoints import item

api_router = APIRouter()
api_router.include_router(meal.router, prefix="/users", tags=["users"])
api_router.include_router(item.router, prefix="/items", tags=["items"])
