from pydantic import BaseModel
from typing import Literal, List, Optional
from datetime import datetime

class UserDietInfo(BaseModel):
    allergy:       Optional[List[str]] = []
    likes:         Optional[List[str]] = []
    dislikes:      Optional[List[str]] = []
    diseases:      Optional[List[str]] = []

class UserDetailsSchema(BaseModel):
    user_id:         int
    gender:          Literal["M","F"]
    age:             int
    height:          Optional[float]
    weight:          float
    meal_count:      Literal["아침","점심","저녁"]
    target_calories: int
    user_diet_info:  UserDietInfo
    created_at:      datetime

    class Config:
        orm_mode = True
