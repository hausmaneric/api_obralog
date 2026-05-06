import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class UserRole(str, enum.Enum):
    owner = "owner"
    engineer = "engineer"
    foreman = "foreman"
    viewer = "viewer"


class WorkStatus(str, enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    paused = "paused"
    finished = "finished"
    cancelled = "cancelled"


class DiaryStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"
    locked = "locked"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cnpj: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(120))
    phone: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    works: Mapped[list["Work"]] = relationship(back_populates="company")
    users: Mapped[list["User"]] = relationship(back_populates="company")
    password_reset_requests: Mapped[list["PasswordResetRequest"]] = relationship(back_populates="company")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.foreman)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company: Mapped["Company"] = relationship(back_populates="users")
    password_reset_requests: Mapped[list["PasswordResetRequest"]] = relationship(back_populates="user")


class Work(Base):
    __tablename__ = "works"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    client_name: Mapped[str | None] = mapped_column(String(120))
    city: Mapped[str | None] = mapped_column(String(80))
    state: Mapped[str | None] = mapped_column(String(2))
    address: Mapped[str | None] = mapped_column(String(255))
    start_date: Mapped[date | None] = mapped_column(Date)
    expected_end_date: Mapped[date | None] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[WorkStatus] = mapped_column(Enum(WorkStatus), default=WorkStatus.planned)
    progress_percentage: Mapped[float] = mapped_column(Float, default=0)

    company: Mapped["Company"] = relationship(back_populates="works")
    diaries: Mapped[list["ConstructionDiary"]] = relationship(back_populates="work")


class ConstructionDiary(Base):
    __tablename__ = "construction_diaries"
    __table_args__ = (UniqueConstraint("work_id", "date", name="uq_work_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    work_id: Mapped[int] = mapped_column(ForeignKey("works.id"), index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    responsible_name: Mapped[str] = mapped_column(String(120), nullable=False)
    weather_morning: Mapped[str | None] = mapped_column(String(80))
    weather_afternoon: Mapped[str | None] = mapped_column(String(80))
    weather_night: Mapped[str | None] = mapped_column(String(80))
    rain: Mapped[str | None] = mapped_column(String(30))
    rain_impact: Mapped[str | None] = mapped_column(Text)
    general_notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[DiaryStatus] = mapped_column(Enum(DiaryStatus), default=DiaryStatus.draft)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    work: Mapped["Work"] = relationship(back_populates="diaries")


class PasswordResetRequest(Base):
    __tablename__ = "password_reset_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    token: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company: Mapped["Company"] = relationship(back_populates="password_reset_requests")
    user: Mapped["User | None"] = relationship(back_populates="password_reset_requests")
