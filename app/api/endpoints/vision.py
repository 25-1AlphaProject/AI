from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.inference import predict
from app.db.session import get_db
from app.models.recipe import Recipe

router = APIRouter()

@router.post("/vision/recognize")
async def recognize_food(
    file: UploadFile = File(..., description="음식 사진"),
    db:   Session    = Depends(get_db)
):
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(400, "이미지 파일을 업로드하세요.")
    img_bytes = await file.read()
    labels = predict(img_bytes)   # e.g. ['apple','kimchi']
    # DB에서 해당 메뉴명 찾아서 calories 리턴
    recipes = db.query(Recipe).filter(Recipe.name.in_(labels)).all()
    return [
        {"name": r.name, "calories": r.calories} 
        for r in recipes
    ]
