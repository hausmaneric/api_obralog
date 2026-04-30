from fastapi import FastAPI

from app.api.router import api_router
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ObraLog API",
    version="0.1.0",
    description="API multiempresa para diario de obra com suporte offline-first.",
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

