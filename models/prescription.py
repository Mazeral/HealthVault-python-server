from sqlalchemy import Enum, Date, func, String, ForeignKey
from sqlalchemy.orm  import Mapped, mapped_column, relationship
import enum
from datetime import date
from typing import List, Optional
from .base import db


class Prescription(db.Model):
    __tablename = "prescription"
    id: Mapped[int] = mapped_column(primary_key=True)
    medication: Mapped[str] = mapped_column(String)
    dosage: Mapped[str] = mapped_column(String)
    instructions: Mapped[Optional[str]] = mapped_column(String)
    prescribedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship(
             # *** CHANGE THIS LINE ***
             back_populates="prescriptions", # Match Patient.prescriptions (this one was already correct based on the attribute name)
             cascade="all" # Keep the previous fix
             )
    # The user relationship below seems correct already
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
             back_populates='prescriptions' # Match User.prescriptions
             )
