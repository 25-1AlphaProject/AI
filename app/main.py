from fastapi import FastAPI
from app.routers import example

app = FastAPI(
    title="척척밥사 AI Server",
    description="AI 서버 및 REST API 통신을 위한 FastAPI 기반 서버",
    version="0.1.0"
)

# API 라우터 등록
app.include_router(example.router, prefix="/api", tags=["example"])

@app.get("/")
def read_root():
    return {"message": "Hello, 척척밥사 AI Server"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
