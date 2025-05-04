from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.db.session           import get_db
from app.models.recipe        import Recipe
from app.models.weekly_meal   import WeeklyMeal
from app.schemas.weekly_meal  import WeeklyMealRead
from app.core.recommendation  import recommend_one_day

router = APIRouter()

@router.post("/recommend/day", response_model=List[WeeklyMealRead])
def recommend_and_save_daily_meal(user: dict, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes in database")

    recommendations = recommend_one_day(user, recipes)
    today = date.today()
    meal_records = []

    for meal_type in ["breakfast", "lunch", "dinner"]:
        rec = recommendations[meal_type]
        new_meal = WeeklyMeal(
            recipe_id=rec["recipe_id"],  # rec["id"]가 아니라 rec["recipe_id"] 로 바꿔야 error 방지
            id2       = user["user_id"],  # user["id"] 대신 user["user_id"] 로 (DB 컬럼명이 id2)
            meal_type = meal_type,
            meal_date = today
        )
        db.add(new_meal)
        meal_records.append(new_meal)

    db.commit()
    for meal in meal_records:
        db.refresh(meal)

    return meal_records
