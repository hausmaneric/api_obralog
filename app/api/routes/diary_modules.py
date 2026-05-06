from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dependencies import get_current_user
from app.models import (
    ConstructionDiary,
    DiaryActivityEntry,
    DiaryEquipmentEntry,
    DiaryMaterialEntry,
    DiaryOccurrenceEntry,
    DiaryPhotoEntry,
    DiaryTeamEntry,
)
from app.schemas import (
    DiaryActivityEntryCreate,
    DiaryActivityEntryRead,
    DiaryEquipmentEntryCreate,
    DiaryEquipmentEntryRead,
    DiaryMaterialEntryCreate,
    DiaryMaterialEntryRead,
    DiaryOccurrenceEntryCreate,
    DiaryOccurrenceEntryRead,
    DiaryPhotoEntryCreate,
    DiaryPhotoEntryRead,
    DiaryTeamEntryCreate,
    DiaryTeamEntryRead,
)

router = APIRouter()


def _ensure_diary(company_id: int, diary_id: int, db: Session) -> ConstructionDiary:
    diary = db.query(ConstructionDiary).filter(ConstructionDiary.id == diary_id, ConstructionDiary.company_id == company_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diario nao encontrado para esta empresa.")
    return diary


@router.get("/teams", response_model=list[DiaryTeamEntryRead])
def list_team_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryTeamEntry).filter(DiaryTeamEntry.company_id == current_user.company_id, DiaryTeamEntry.diary_id == diary_id).order_by(DiaryTeamEntry.id.desc()).all()


@router.post("/teams", response_model=DiaryTeamEntryRead)
def create_team_entry(payload: DiaryTeamEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar equipe para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryTeamEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/teams/{entry_id}", status_code=204)
def delete_team_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryTeamEntry).filter(DiaryTeamEntry.id == entry_id, DiaryTeamEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de equipe nao encontrado.")
    db.delete(entry)
    db.commit()


@router.get("/activities", response_model=list[DiaryActivityEntryRead])
def list_activity_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryActivityEntry).filter(DiaryActivityEntry.company_id == current_user.company_id, DiaryActivityEntry.diary_id == diary_id).order_by(DiaryActivityEntry.id.desc()).all()


@router.post("/activities", response_model=DiaryActivityEntryRead)
def create_activity_entry(payload: DiaryActivityEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar atividade para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryActivityEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/activities/{entry_id}", status_code=204)
def delete_activity_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryActivityEntry).filter(DiaryActivityEntry.id == entry_id, DiaryActivityEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de atividade nao encontrado.")
    db.delete(entry)
    db.commit()


@router.get("/materials", response_model=list[DiaryMaterialEntryRead])
def list_material_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryMaterialEntry).filter(DiaryMaterialEntry.company_id == current_user.company_id, DiaryMaterialEntry.diary_id == diary_id).order_by(DiaryMaterialEntry.id.desc()).all()


@router.post("/materials", response_model=DiaryMaterialEntryRead)
def create_material_entry(payload: DiaryMaterialEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar material para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryMaterialEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/materials/{entry_id}", status_code=204)
def delete_material_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryMaterialEntry).filter(DiaryMaterialEntry.id == entry_id, DiaryMaterialEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de material nao encontrado.")
    db.delete(entry)
    db.commit()


@router.get("/equipments", response_model=list[DiaryEquipmentEntryRead])
def list_equipment_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryEquipmentEntry).filter(DiaryEquipmentEntry.company_id == current_user.company_id, DiaryEquipmentEntry.diary_id == diary_id).order_by(DiaryEquipmentEntry.id.desc()).all()


@router.post("/equipments", response_model=DiaryEquipmentEntryRead)
def create_equipment_entry(payload: DiaryEquipmentEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar equipamento para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryEquipmentEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/equipments/{entry_id}", status_code=204)
def delete_equipment_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryEquipmentEntry).filter(DiaryEquipmentEntry.id == entry_id, DiaryEquipmentEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de equipamento nao encontrado.")
    db.delete(entry)
    db.commit()


@router.get("/occurrences", response_model=list[DiaryOccurrenceEntryRead])
def list_occurrence_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryOccurrenceEntry).filter(DiaryOccurrenceEntry.company_id == current_user.company_id, DiaryOccurrenceEntry.diary_id == diary_id).order_by(DiaryOccurrenceEntry.id.desc()).all()


@router.post("/occurrences", response_model=DiaryOccurrenceEntryRead)
def create_occurrence_entry(payload: DiaryOccurrenceEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar ocorrencia para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryOccurrenceEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/occurrences/{entry_id}", status_code=204)
def delete_occurrence_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryOccurrenceEntry).filter(DiaryOccurrenceEntry.id == entry_id, DiaryOccurrenceEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de ocorrencia nao encontrado.")
    db.delete(entry)
    db.commit()


@router.get("/photos", response_model=list[DiaryPhotoEntryRead])
def list_photo_entries(diary_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ensure_diary(current_user.company_id, diary_id, db)
    return db.query(DiaryPhotoEntry).filter(DiaryPhotoEntry.company_id == current_user.company_id, DiaryPhotoEntry.diary_id == diary_id).order_by(DiaryPhotoEntry.id.desc()).all()


@router.post("/photos", response_model=DiaryPhotoEntryRead)
def create_photo_entry(payload: DiaryPhotoEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if payload.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Nao e permitido criar foto para outra empresa.")
    _ensure_diary(current_user.company_id, payload.diary_id, db)
    entry = DiaryPhotoEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/photos/{entry_id}", status_code=204)
def delete_photo_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(DiaryPhotoEntry).filter(DiaryPhotoEntry.id == entry_id, DiaryPhotoEntry.company_id == current_user.company_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Registro de foto nao encontrado.")
    db.delete(entry)
    db.commit()
