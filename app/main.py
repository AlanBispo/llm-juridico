from fastapi import FastAPI
from app.api.endpoints import triagem
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Juridic Strategic API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Rota triagem
app.include_router(triagem.router, prefix="/triagem", tags=["Jurídico"])

@app.get("/")
async def root():
    return {"status": "online", "message": "API Jurídica Operacional"}