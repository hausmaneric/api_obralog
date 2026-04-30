from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.seed import seed_demo_data

router = APIRouter()


@router.post("/seed")
def seed(db: Session = Depends(get_db)):
    return seed_demo_data(db)
