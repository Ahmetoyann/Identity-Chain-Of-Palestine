from fastapi import APIRouter

from app.v1.endpoints.health import router as health_router
from app.v1.endpoints.items import router as prisoners_router
from app.v1.endpoints.contact import router as contact_router
from app.v1.endpoints.matches import router as matches_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(prisoners_router)
api_router.include_router(contact_router)
api_router.include_router(matches_router)
