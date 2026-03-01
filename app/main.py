from fastapi import FastAPI
from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Juridic Strategic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Inclui as rotas
app.include_router(api_router)
