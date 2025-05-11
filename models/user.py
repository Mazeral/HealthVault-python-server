import Base from .base
from sqlalchemy import Enum, Date, func
import enum
from datetime import date
from typing import List


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[Role] = mapped_column(Enum(Role))
    createdAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    updatedAt: Mapped[date] = mapped_column(Date, server_default=func.now())
    # This is the "many" side, where we have many patients
    patients: Mapped[List["Patient"]] = relationship(
            # The back_populates argument here should match the attribute
            # name you used on the "one" side.
            back_populates="user",
            cascade="all, delete-orphan"
            )
    medicalRecords: Mapped[List["MedicalRecord"]] = relationship(
            back_populates="user",
            cascade="all, delete-orphan"
            )
    prescriptions: Mapped[List["Prescription"]] = relationship(
            back_populates="user",
            cascade="all, delete-orphan"
            )
    labResults: Mapped[List["LabResult"]] = relationship(
            back_populates="user",
            cascade="all, delete-orphan"
            )
