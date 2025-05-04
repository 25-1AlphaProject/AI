from fastapi import APIRouter
from datetime import datetime, timedelta
from app.core.recommendation import recommend_one_day

router = APIRouter()

@router.get("/meal/ingredient-links/{reciped}")
def create_weekly_meal_plan(user: dict):
    
    return {
        
    }
