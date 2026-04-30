from datetime import date

from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str
    cnpj: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class CompanyRead(CompanyCreate):
    id: int

    class Config:
        from_attributes = True


class WorkCreate(BaseModel):
    company_id: int
    name: str
    code: str
    client_name: str | None = None
    city: str | None = None
    state: str | None = None
    address: str | None = None
    progress_percentage: float = Field(default=0, ge=0, le=100)


class WorkRead(WorkCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryCreate(BaseModel):
    company_id: int
    work_id: int
    date: date
    number: str
    responsible_name: str
    weather_morning: str | None = None
    weather_afternoon: str | None = None
    weather_night: str | None = None
    rain: str | None = None
    rain_impact: str | None = None
    general_notes: str | None = None


class DiaryRead(DiaryCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str
    company_id: int


class LoginResponse(BaseModel):
    access_token: str
    user_id: int
    company_id: int
    role: str
    name: str
