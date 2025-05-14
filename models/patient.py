from sqlalchemy import Enum, Date, func, String, ForeignKey
from sqlalchemy.orm  import Mapped, mapped_column, relationship
import enum
from datetime import date
from typing import List, Optional
from .base import db


class Sex(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class BloodGroup(enum.Enum):
    A_PLUS = "A+"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B_MINUS = "B-"
    AB_PLUS = "AB+"
    AB_MINUS = "AB-"
    O_PLUS = "O+"
    O_MINUS = "O-"


class Patient(db.Model):
    __tablename__ = "patient"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullName: Mapped[str] = mapped_column(String, unique=True)
    dateOfBirth: Mapped[date] = mapped_column(Date)
    phone: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(String)
    createdAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    updatedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    sex: Mapped[Sex] = mapped_column(Enum(Sex))
    bloodGroup: Mapped[BloodGroup] = mapped_column(Enum(BloodGroup))
    medicalRecords: Mapped[List["MedicalRecord"]] = relationship(
                back_populates="patient",
                cascade="all, delete-orphan"
            )
    prescriptions: Mapped[List["Prescription"]] = relationship(
                back_populates="patient",
                cascade="all, delete-orphan"
            )
    labResults: Mapped[List["LabResult"]] = relationship(
                back_populates="patient",
                cascade="all, delete-orphan"
            )
    # in n-1 relations, we create a foreign key col, and a relation col to hold
    # a single object of the other side of the relation
    # User here is the table name
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="patients")
