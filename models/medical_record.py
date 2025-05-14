from .base import db
from sqlalchemy import Enum, Date, func
import enum
from datetime import date
from typing import List, Optional


class MedicalRecord(db.Model):
    # naming in snake_case is the convention in sqlalchemy
    __tablename__ = "medical_record"
    id: Mapped[int] = mapped_column(primary_key=True)
    patientId: Mapped[int]
    diagnosis: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(String)
    createdAt: Mapped[date] = mapped_column(date, server_default=func.now())
    updatedAt: Mapped[date] = mapped_column(date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relation(
            back_populates="medical_records",
            cascasde="all, delete-orphan"
            )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relation(
            back_populates="medical_records",
            cascasde="all, delete-orphan"
            )
