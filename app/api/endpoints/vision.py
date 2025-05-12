from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.inference import predict
from app.db.session import get_db
from app.models.recipe import Recipe
from pathlib import Path

router = APIRouter()

@router.post("/recognize", summary="이미지를 받아 음식 레이블만 반환")
async def recognize_food(
    file: UploadFile = File(..., description="음식 사진 (multipart/form-data)")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "이미지 파일을 업로드하세요.")
    img_bytes = await file.read()
    labels = predict(img_bytes)
    return {"labels": labels}