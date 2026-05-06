from fastapi import APIRouter

from app.api.routes import auth, bootstrap, companies, diaries, diary_modules, passwords, users, works

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(bootstrap.router, prefix="/bootstrap", tags=["bootstrap"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(passwords.router, prefix="/passwords", tags=["passwords"])
api_router.include_router(works.router, prefix="/works", tags=["works"])
api_router.include_router(diaries.router, prefix="/diaries", tags=["diaries"])
api_router.include_router(diary_modules.router, prefix="/diary-modules", tags=["diary-modules"])
