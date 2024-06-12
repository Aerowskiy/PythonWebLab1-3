import uvicorn
from fastapi import FastAPI, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.deals import router as orders_router
from app.routers.reviews import router as reviews_router
from app.routers.users import router as users_router

app = FastAPI(title="Repair Workshop")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client['repair_workshop']


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


router = APIRouter(tags=["Health Check"])


@router.get("/health")
def health_check():
    return {"status_code": 200, "detail": "ok", "result": "working"}


app.include_router(router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(reviews_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
