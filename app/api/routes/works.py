from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import Work
from app.schemas import WorkCreate, WorkRead

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
