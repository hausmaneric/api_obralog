from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import User


def get_current_user(
    x_company_id: int | None = Header(default=None),
    x_user_id: int | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if x_company_id is None or x_user_id is None:
        raise HTTPException(status_code=401, detail="Cabecalhos de autenticacao ausentes.")

    user = (
        db.query(User)
        .filter(User.id == x_user_id, User.company_id == x_company_id, User.status == "active")
        .first()
    )
    if not user:
        raise HTTPException(status_code=401, detail="Usuario invalido para a empresa informada.")
    return user
