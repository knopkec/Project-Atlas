"""SQLAlchemy ORM models."""

import uuid

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    departments: Mapped[list["Department"]] = relationship(back_populates="hospital")


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hospital_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hospitals.id"), nullable=False
    )

    hospital: Mapped["Hospital"] = relationship(back_populates="departments")
    meetings: Mapped[list["Meeting"]] = relationship(back_populates="department")


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    transcript: Mapped[str] = mapped_column(Text, default="", nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id"), nullable=False
    )

    department: Mapped["Department"] = relationship(back_populates="meetings")
