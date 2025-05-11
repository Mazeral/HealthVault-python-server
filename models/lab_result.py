import Base from .base
from sqlalchemy import Enum, Date, func
import enum
from datetime import date
from typing import List, Optional


class LabResult(Base):
    __tablename__ = "lab_result"
    id: Mapped[int] = mapped_column(primary_key=True)
    testName: Mapped[str] = mapped_column(String)
    result: Mapped[str] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(String)
    performedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    createdAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    patientId: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relation(
            back_populates="lab_results",
            cascasde="all, delete-orphan"
            )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relation(
            back_populates="lab_results",
            cascasde="all, delete-orphan"
            )
