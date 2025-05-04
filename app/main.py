from fastapi import FastAPI
from app.api.endpoints import meal
from app.routers import example
from fastapi.responses import PlainTextResponse
from fastapi import Request
import traceback


app = FastAPI(
    title="척척밥사 AI Server",
    description="AI 서버 및 REST API 통신을 위한 FastAPI 기반 서버",
    version="0.1.0"
)

app.include_router(example.router, prefix="/api", tags=["example"])
app.include_router(meal.router, prefix="/api/meal", tags=["meal"])


@app.get("/")
def read_root():
    return {"message": "Hello, 척척밥사 AI Server"}

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()               
    return PlainTextResponse(
        content=f"{type(exc).__name__}: {exc}", 
        status_code=500
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
