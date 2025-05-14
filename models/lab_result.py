from sqlalchemy import Enum, Date, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from datetime import date
from typing import List, Optional
from .base import db


class LabResult(db.Model):
    __tablename__ = "lab_result"
    id: Mapped[int] = mapped_column(primary_key=True)
    testName: Mapped[str] = mapped_column(String)
    result: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(String)
    performedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    createdAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship(
             # *** CHANGE THIS LINE ***
             back_populates="labResults", # Match Patient.labResults
             cascade="all" # Keep the previous fix
             )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
             # *** CHANGE THIS LINE ***
             back_populates="labResults", # Match User.labResults
             cascade="all" # Keep the previous fix
             )
