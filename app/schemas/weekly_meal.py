from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum as PyEnum
from typing import Optional

class MealType(str, PyEnum):
    breakfast = "BREAKFAST"
    lunch     = "LUNCH"
    dinner    = "DINNER"
    snack     = "SNACK"

class WeeklyMealCreate(BaseModel):
    recipe_id: int
    user_id:  int
    meal_type: MealType
    meal_date: date
    created_at: date

class WeeklyMealRead(WeeklyMealCreate):
    meal_id:         int
    created_at: Optional[datetime] = None   

    class Config:
        orm_mode = True
