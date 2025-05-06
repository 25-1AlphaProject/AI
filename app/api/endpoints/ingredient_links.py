from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
import re

from app.db.session import get_db
from app.models.recipe import Recipe

router = APIRouter()

def _parse_ingredients(raw: str) -> List[str]:
    """
    1) 줄바꿈, ●, -, : 등을 구분자로 분리
    2) 쉼표(,)로 추가 분리
    3) 각 세그먼트에서 '(…)'나 숫자+단위 이후 텍스트를 잘라내 재료명만 추출
    4) 빈 문자열·중복 제거
    """
    parts = re.split(r"[\n●\-:]+", raw)
    candidates = []
    for part in parts:
        for seg in part.split(","):
            seg = seg.strip()
            if seg:
                candidates.append(seg)

    names = set()
    for seg in candidates:
        name = re.split(r"[\(\d]", seg)[0].strip()
        if name:
            names.add(name)
    return list(names)


@router.get(
    "/ingredient-links/{recipe_id}",
    response_model=List[Dict[str,str]],
    summary="레시피의 재료별로 쿠팡 검색 링크를 생성해 반환"
)
def ingredient_links(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    raw = recipe.ingredient or ""
    names = _parse_ingredients(raw)
    base = "https://www.coupang.com/np/search?component=&q={q}&channel=user"
    result = []
    for name in names:
        link = base.format(q=name)
        result.append({"ingredient": name, "link": link})

    return result
