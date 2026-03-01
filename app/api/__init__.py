from fastapi import APIRouter
from . import processo 

api_router = APIRouter()

api_router.include_router(processo.router)
