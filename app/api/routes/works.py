from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from fastapi import HTTPException

from app.models import Work
from app.schemas import WorkCreate, WorkRead, WorkUpdate

router = APIRouter()


@router.get("/", response_model=list[WorkRead])
def list_works(
    company_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Work).filter(Work.company_id == current_user.company_id)
    if company_id:
        query = query.filter(Work.company_id == company_id)
    return query.order_by(Work.name).all()


@router.post("/", response_model=WorkRead)
def create_work(payload: WorkCreate, db: Session = Depends(get_db)):
    work = Work(**payload.model_dump())
    db.add(work)
    db.commit()
    db.refresh(work)
    return work


@router.patch("/{work_id}", response_model=WorkRead)
def update_work(work_id: int, payload: WorkUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    work = db.query(Work).filter(Work.id == work_id, Work.company_id == current_user.company_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Obra nao encontrada.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(work, field, value)

    db.add(work)
    db.commit()
    db.refresh(work)
    return work


@router.delete("/{work_id}", status_code=204)
def delete_work(work_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    work = db.query(Work).filter(Work.id == work_id, Work.company_id == current_user.company_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Obra nao encontrada.")
    db.delete(work)
    db.commit()
