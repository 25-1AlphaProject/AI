from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum as PyEnum
from typing import Optional

class MealType(str, PyEnum):
    breakfast = "breakfast"
    lunch     = "lunch"
    dinner    = "dinner"
    snack     = "snack"

class WeeklyMealCreate(BaseModel):
    recipe_id: int
    id2:       int
    meal_type: MealType
    meal_date: date

class WeeklyMealRead(WeeklyMealCreate):
    id:         int
    created_at: Optional[datetime] = None   

    class Config:
        orm_mode = True
