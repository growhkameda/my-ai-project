# src/backend/routers/__init__.py
from fastapi import APIRouter

from src.backend.routers.auth import router as auth_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

__all__ = ["api_router"]
