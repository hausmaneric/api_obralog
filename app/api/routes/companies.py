from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import Company
from app.schemas import CompanyCreate, CompanyRead

router = APIRouter()


@router.get("/", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Company).filter(Company.id == current_user.company_id).order_by(Company.name).all()


@router.post("/", response_model=CompanyRead)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
