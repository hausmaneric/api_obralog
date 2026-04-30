from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_cors_origins, settings
from app.core.db import Base, engine

if settings.auto_create_tables:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ObraLog API",
    version="0.1.0",
    description="API multiempresa para diario de obra com suporte offline-first.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
