from sqlalchemy import Enum, Date, func
import enum
from datetime import date
from typing import List, Optional
import db from .base


class Prescription(db.Model):
    __tablename = "prescription"
    id: Mapped[int] = mapped_column(primary_key=True)
    medication: Mapped[str] = mapped_column(String)
    dosage: Mapped[str] = mapped_column(String)
    instructions: Mapped[Optional[str]] = mapped_column(String)
    prescribedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship(
            back_populates="prescriptions",
            cascade="all, delete-orphan"
            )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
            back_populates='prescriptions'
            )
