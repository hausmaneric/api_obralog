from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse
from app.security import create_access_token, verify_password

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            User.email == payload.email,
            User.company_id == payload.company_id,
            User.status == "active",
        )
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais invalidas.")

    token = create_access_token(user.id, user.company_id, user.role.value)
    return LoginResponse(
        access_token=token,
        user_id=user.id,
        company_id=user.company_id,
        role=user.role.value,
        name=user.name,
    )
