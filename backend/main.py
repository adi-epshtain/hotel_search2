from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.search import router as search_router
from app.routers.health import router as health_router

app = FastAPI(title="Hotel Search Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/api/search")
app.include_router(health_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

