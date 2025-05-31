from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.core.inference import predict
from app.db.session import get_db
from app.models.recipe import Recipe
from app.schemas.vision  import RecognizeRequest, RecognizeResponse
from app.core.label_map   import translate_label

from pathlib import Path
import requests
import random


router = APIRouter()

@router.post(
    "/recognize",
    response_model=RecognizeResponse,
    summary="음식 인식하기"
)
def recognize_food(
    req: RecognizeRequest = Body(..., description="mealPhoto: 이미지 URL, amount: 인분 수"),
    db:  Session          = Depends(get_db)
):
    try:
        resp = requests.get(req.mealPhoto, timeout=5)
        resp.raise_for_status()
        img_bytes = resp.content
    except Exception:
        raise HTTPException(400, "mealPhoto URL 에서 이미지를 불러올 수 없습니다.")

    eng_labels = predict(img_bytes) 
    if not eng_labels:
        raise HTTPException(404, "음식을 인식할 수 없습니다.")

    eng = eng_labels[0]
    ko  = translate_label(eng)     

    candidates = (
        db.query(Recipe)
          .filter(Recipe.name.ilike(f"%{ko}%"))
          .all()
    )
    if not candidates:
        raise HTTPException(404, f"‘{ko}’ 메뉴를 찾을 수 없습니다.")

    pick = random.choice(candidates)

    return {
        "mealName":     ko,           
        "foodCalories": pick.calories,
        "protein" : pick.protein,
        "fat": pick.fat,
        "carbohydrate": pick.carbohydrates,

    }