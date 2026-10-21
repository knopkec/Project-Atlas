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


class WorkflowCreate(BaseModel):
    description: str


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    description: str
    department_id: uuid.UUID
    meeting_id: uuid.UUID


class ProblemCreate(BaseModel):
    title: str
    description: str = ""
    workflow_id: uuid.UUID | None = None


class ProblemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    department_id: uuid.UUID
    meeting_id: uuid.UUID
    workflow_id: uuid.UUID | None


class AdoptionRiskCreate(BaseModel):
    title: str
    description: str = ""


class AdoptionRiskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    department_id: uuid.UUID
    meeting_id: uuid.UUID


class StakeholderCreate(BaseModel):
    name: str
    role: str = ""


class StakeholderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    role: str
    department_id: uuid.UUID


class StakeholderLink(BaseModel):
    stakeholder_id: uuid.UUID
