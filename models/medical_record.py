from .base import db
from sqlalchemy import Enum, Date, func, String, ForeignKey
from sqlalchemy.orm  import Mapped, mapped_column, relationship
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
    createdAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    updatedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship(
             # *** CHANGE THIS LINE ***
             back_populates="medicalRecords", # Match Patient.medicalRecords
             cascade="all" # Keep the previous fix
             )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
             # *** CHANGE THIS LINE ***
             back_populates="medicalRecords", # Match User.medicalRecords
             cascade="all" # Keep the previous fix
             )
