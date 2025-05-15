from pydantic import BaseModel, HttpUrl, conint, confloat

class RecognizeRequest(BaseModel):
    mealPhoto: HttpUrl
    amount:   float

class RecognizeResponse(BaseModel):
    mealName:     str
    foodCalories: float