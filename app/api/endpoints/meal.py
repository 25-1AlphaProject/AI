# app/api/endpoints/meal.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.db.session           import get_db
from app.models.recipe        import Recipe
from app.models.weekly_meal   import WeeklyMeal
from app.schemas.user         import UserDetailsSchema
from app.core.recommendation  import recommend_one_day

router = APIRouter()

@router.post(
    "/weekly",
    response_model=dict,  
    summary="사용자 정보를 받아 일주일치 식단을 추천·생성."
)
def create_weekly_plan(
    user: UserDetailsSchema = Body(..., description="사용자 상세 정보"),
    db: Session            = Depends(get_db),
):
    recipes = db.query(Recipe).all()
    if not recipes:
        raise HTTPException(404, "레시피가 없습니다.")

    today = date.today()
    for offset in range(7):
        meal_date = today + timedelta(days=offset)
        recs = recommend_one_day(user.dict(), recipes)

        for meal_type in ("BREAKFAST", "LUNCH", "DINNER"):
            r = recs[meal_type]
            wm = WeeklyMeal(
                recipe_id  = r["recipe_id"],
                user_id    = user.user_id,
                meal_type  = meal_type,
                meal_date  = meal_date,
                created_at = date.today()
            )
            db.add(wm)

    db.commit()

    return {"success": True}