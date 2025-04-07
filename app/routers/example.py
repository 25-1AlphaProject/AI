from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"message": "안녕하세요, 척척밥사 프로젝트입니다!"}
