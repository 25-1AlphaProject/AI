from pydantic import BaseModel
from typing import Literal, List, Optional
from datetime import datetime
from enum import Enum as PyEnum

class MealCount(str, PyEnum):
    BREAKFAST = "BREAKFAST"
    LUNCH     = "LUNCH"
    DINNER    = "DINNER"

class UserDietInfo(BaseModel):
    allergies:       Optional[List[str]] = []
    preferredMenus:         Optional[List[str]] = []
    avoidIngredients:      Optional[List[str]] = []
    diseases:      Optional[List[str]] = []

class HealthGoal(str, PyEnum):
    DIET                = "DIET"
    DISEASE_MANAGEMENT  = "DISEASE_MANAGEMENT"
    HABIT_IMPROVEMENT   = "HABIT_IMPROVEMENT"
    NOT_SURE            = "NOT_SURE"

class UserDetailsSchema(BaseModel):
    user_id:         int
    gender:          Literal["M","F"]
    age:             int
    height:          Optional[float]
    weight:          float
    meal_count:      List[MealCount]
    target_calories: int
    user_diet_info:  UserDietInfo
    health_goal:     Optional[HealthGoal] = None  

    class Config:
        orm_mode = True
