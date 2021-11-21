from fastapi import APIRouter

from app.quotes import api as quotes_api

api_router = APIRouter()

api_router.include_router(quotes_api.router, prefix="/quotes", tags=["Quotes"])
