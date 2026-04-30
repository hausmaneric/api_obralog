from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import ConstructionDiary
from app.schemas import DiaryCreate, DiaryRead

router = APIRouter()


@router.get("/", response_model=list[DiaryRead])
def list_diaries(
    work_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(ConstructionDiary).filter(ConstructionDiary.company_id == current_user.company_id)
    if work_id:
        query = query.filter(ConstructionDiary.work_id == work_id)
    return query.order_by(ConstructionDiary.date.desc()).all()


@router.post("/", response_model=DiaryRead)
def create_diary(payload: DiaryCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(ConstructionDiary)
        .filter(
            ConstructionDiary.work_id == payload.work_id,
            ConstructionDiary.date == payload.date,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Ja existe um diario para essa obra e data.")

    diary = ConstructionDiary(**payload.model_dump())
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary
