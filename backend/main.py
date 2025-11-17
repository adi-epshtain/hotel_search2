from fastapi import FastAPI
from app.routers.search import router as search_router
from app.routers.health import router as health_router

app = FastAPI(title="Hotel Search Service")
app.include_router(search_router, prefix="/api/search")
app.include_router(health_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

