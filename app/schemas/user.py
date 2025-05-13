from pydantic import BaseModel
from typing import Literal, List, Optional
from datetime import datetime

class UserDietInfo(BaseModel):
    allergies:       Optional[List[str]] = []
    preferredMenus:         Optional[List[str]] = []
    avoidIngredients:      Optional[List[str]] = []
    diseases:      Optional[List[str]] = []
    health_goal: Literal["DIET","DISEASE_MANAGEMENT","HABIT_IMPROVEMENT","NOT_SURE"]  


class UserDetailsSchema(BaseModel):
    user_id:         int
    gender:          Literal["M","F"]
    age:             int
    height:          Optional[float]
    weight:          float
    meal_count:      Literal["BREAKFAST","LUNCH","DINNER"]
    target_calories: int
    user_diet_info:  UserDietInfo

    class Config:
        orm_mode = True
