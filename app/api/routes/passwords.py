import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import PasswordResetRequest, User
from app.schemas import PasswordResetRequestCreate, PasswordResetRequestRead

router = APIRouter()


@router.post("/forgot", response_model=PasswordResetRequestRead)
def request_password_reset(payload: PasswordResetRequestCreate, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            User.company_id == payload.company_id,
            User.email == payload.email,
        )
        .first()
    )
    request = PasswordResetRequest(
        company_id=payload.company_id,
        user_id=user.id if user else None,
        email=payload.email,
        token=secrets.token_urlsafe(24),
        status="pending",
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request
