from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import User, UserRole
from app.schemas import UserCreate, UserRead, UserUpdate
from app.security import hash_password

router = APIRouter()


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    users = db.query(User).filter(User.company_id == current_user.company_id).order_by(User.name).all()
    return [
        UserRead(
            id=user.id,
            company_id=user.company_id,
            name=user.name,
            email=user.email,
            role=user.role.value,
            status=user.status,
        )
        for user in users
    ]


@router.post("/", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar usuario para outra empresa.")
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ja existe usuario com este e-mail.")

    user = User(
        company_id=payload.company_id,
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        status="active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(
        id=user.id,
        company_id=user.company_id,
        name=user.name,
        email=user.email,
        role=user.role.value,
        status=user.status,
    )


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id, User.company_id == current_user.company_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado.")

    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password_hash = hash_password(data["password"])
    if "role" in data:
        user.role = UserRole(data["role"])
    if "status" in data:
        user.status = data["status"]

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(
        id=user.id,
        company_id=user.company_id,
        name=user.name,
        email=user.email,
        role=user.role.value,
        status=user.status,
    )


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id, User.company_id == current_user.company_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado.")
    db.delete(user)
    db.commit()
