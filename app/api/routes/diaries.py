from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import ConstructionDiary
from app.schemas import DiaryCreate, DiaryRead, DiaryUpdate

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


@router.patch("/{diary_id}", response_model=DiaryRead)
def update_diary(diary_id: int, payload: DiaryUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    diary = db.query(ConstructionDiary).filter(ConstructionDiary.id == diary_id, ConstructionDiary.company_id == current_user.company_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diario nao encontrado.")

    data = payload.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        diary.status = data["status"]
        data.pop("status")

    for field, value in data.items():
        setattr(diary, field, value)

    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary


@router.delete("/{diary_id}", status_code=204)
def delete_diary(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    diary = db.query(ConstructionDiary).filter(ConstructionDiary.id == diary_id, ConstructionDiary.company_id == current_user.company_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diario nao encontrado.")
    db.delete(diary)
    db.commit()
