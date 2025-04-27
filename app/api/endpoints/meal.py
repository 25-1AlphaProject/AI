from fastapi import APIRouter
from datetime import datetime, timedelta
from app.core.recommendation import recommend_one_day

router = APIRouter()

@router.post("/meal/weekly")
def create_weekly_meal_plan(user: dict):
    """
    일주일치 식단 추천 API
    """
    today = datetime.today()
    meal_plan = []

    for i in range(7):
        meal_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        daily_meal = recommend_one_day(user)
        daily_meal["meal_date"] = meal_date
        meal_plan.append(daily_meal)
    
    return {
        "created_at": today.strftime("%Y-%m-%d"),
        "meal_plan": meal_plan
    }
