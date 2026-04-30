from fastapi import APIRouter

from app.api.routes import auth, bootstrap, companies, diaries, works

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(bootstrap.router, prefix="/bootstrap", tags=["bootstrap"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(works.router, prefix="/works", tags=["works"])
api_router.include_router(diaries.router, prefix="/diaries", tags=["diaries"])
