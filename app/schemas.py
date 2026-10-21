"""Pydantic request/response schemas."""

import uuid

from pydantic import BaseModel, ConfigDict


class HospitalCreate(BaseModel):
    name: str


class HospitalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class DepartmentCreate(BaseModel):
    name: str


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    hospital_id: uuid.UUID


class MeetingCreate(BaseModel):
    title: str
    transcript: str = ""


class MeetingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    transcript: str
    department_id: uuid.UUID
