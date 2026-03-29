from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import DomainError

app = FastAPI(title="Juridic Strategic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Inclui as rotas
app.include_router(api_router)
