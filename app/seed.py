from datetime import date

from sqlalchemy.orm import Session

from app.models import Company, ConstructionDiary, DiaryStatus, User, UserRole, Work, WorkStatus
from app.security import hash_password


def seed_demo_data(db: Session) -> dict[str, int | str]:
    company = db.query(Company).filter(Company.name == "Construtora Alfa").first()
    if company:
        return {"company_id": company.id, "user_email": "engenheiro@obralog.com"}

    company = Company(
        name="Construtora Alfa",
        cnpj="12.345.678/0001-90",
        email="contato@alfa.com",
        phone="(11) 99999-0000",
        address="Rua das Flores, 123",
    )
    db.add(company)
    db.flush()

    user = User(
        company_id=company.id,
        name="Eric Silva",
        email="engenheiro@obralog.com",
        password_hash=hash_password("123456"),
        role=UserRole.engineer,
    )
    db.add(user)

    works = [
        Work(
            company_id=company.id,
            name="Reforma Escola Central",
            code="OBR-001",
            client_name="Prefeitura Municipal",
            city="Sao Paulo",
            state="SP",
            address="Rua das Flores, 123",
            status=WorkStatus.in_progress,
            progress_percentage=70,
        ),
        Work(
            company_id=company.id,
            name="Residencial Vila Verde",
            code="OBR-002",
            client_name="Construtora Silva",
            city="Campinas",
            state="SP",
            address="Av. Verde, 88",
            status=WorkStatus.in_progress,
            progress_percentage=45,
        ),
    ]
    db.add_all(works)
    db.flush()

    db.add(
        ConstructionDiary(
            company_id=company.id,
            work_id=works[0].id,
            date=date(2026, 4, 30),
            number="00045",
            responsible_name="Eric Silva",
            weather_morning="Ensolarado",
            weather_afternoon="Chuva leve",
            weather_night="Sem atividade",
            rain="partial",
            rain_impact="A chuva atrapalhou a concretagem da laje entre 13h e 15h.",
            general_notes="Cliente solicitou ajuste no acabamento do banheiro.",
            status=DiaryStatus.draft,
        )
    )
    db.commit()
    return {"company_id": company.id, "user_email": user.email}
