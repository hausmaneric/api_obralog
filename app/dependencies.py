from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import User
from app.security import decode_access_token


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Cabecalho Authorization ausente.")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de Authorization invalido.")

    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    company_id = int(payload["company_id"])

    user = (
        db.query(User)
        .filter(User.id == user_id, User.company_id == company_id, User.status == "active")
        .first()
    )
    if not user:
        raise HTTPException(status_code=401, detail="Usuario invalido para a empresa informada.")
    return user
