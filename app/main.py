from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import traceback

from app.api.endpoints.meal             import router as meal_router
from app.api.endpoints.ingredient_links import router as ing_router
from app.api.endpoints.vision           import router as vision_router
from app.routers.example                import router as example_router
from app.core.inference                 import load_model

app = FastAPI(
    title="척척밥사 AI Server",
    description="AI 서버 및 REST API 통신을 위한 FastAPI 기반 서버",
    version="0.1.0"
)

app.include_router(example_router, prefix="/api",              tags=["example"])
app.include_router(meal_router,    prefix="/api/meal",         tags=["meal"])
app.include_router(ing_router,     prefix="/api/ingredient",   tags=["ingredient-links"])
app.include_router(vision_router,  prefix="/api/vision",       tags=["vision"])

@app.get("/")
def read_root():
    return {"message": "Hello, 척척밥사 AI Server"}

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return PlainTextResponse(f"{type(exc).__name__}: {exc}", status_code=500)

@app.on_event("startup")
def on_startup():
    load_model()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
