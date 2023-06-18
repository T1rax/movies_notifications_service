from fastapi import APIRouter
from src.api.v1.endpoints import users


router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(users.router)
