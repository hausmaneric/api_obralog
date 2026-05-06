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


class CompanyUpdate(BaseModel):
    name: str | None = None
    cnpj: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


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


class WorkUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    client_name: str | None = None
    city: str | None = None
    state: str | None = None
    address: str | None = None
    progress_percentage: float | None = Field(default=None, ge=0, le=100)


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


class DiaryUpdate(BaseModel):
    number: str | None = None
    responsible_name: str | None = None
    weather_morning: str | None = None
    weather_afternoon: str | None = None
    weather_night: str | None = None
    rain: str | None = None
    rain_impact: str | None = None
    general_notes: str | None = None
    status: str | None = None


class DiaryTeamEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    total_workers: int = 0
    total_hours: int = 0
    highlight_role: str | None = None


class DiaryTeamEntryRead(DiaryTeamEntryCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryActivityEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    title: str
    status: str = "Em andamento"
    progress: int = 0


class DiaryActivityEntryRead(DiaryActivityEntryCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryMaterialEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    material_name: str
    quantity_label: str | None = None
    movement_type: str = "Recebido"


class DiaryMaterialEntryRead(DiaryMaterialEntryCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryEquipmentEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    equipment_name: str
    status: str = "Parado"
    usage_hours: str | None = None


class DiaryEquipmentEntryRead(DiaryEquipmentEntryCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryOccurrenceEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    title: str
    description: str | None = None
    responsible: str | None = None
    action_taken: str | None = None
    status: str = "Aberta"
    severity: str = "Baixa"


class DiaryOccurrenceEntryRead(DiaryOccurrenceEntryCreate):
    id: int

    class Config:
        from_attributes = True


class DiaryPhotoEntryCreate(BaseModel):
    company_id: int
    diary_id: int
    title: str
    category: str | None = None
    location: str | None = None
    file_url: str | None = None


class DiaryPhotoEntryRead(DiaryPhotoEntryCreate):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str
    company_id: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: int
    company_id: int
    role: str
    name: str


class UserCreate(BaseModel):
    company_id: int
    name: str
    email: str
    password: str
    role: str = "foreman"


class UserRead(BaseModel):
    id: int
    company_id: int
    name: str
    email: str
    role: str
    status: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    status: str | None = None


class PasswordResetRequestCreate(BaseModel):
    company_id: int
    email: str


class PasswordResetRequestRead(BaseModel):
    id: int
    company_id: int
    user_id: int | None = None
    email: str
    token: str
    status: str

    class Config:
        from_attributes = True
