from fastapi import APIRouter
from . import processo, chat

api_router = APIRouter()

api_router.include_router(processo.router)
api_router.include_router(chat.router)
