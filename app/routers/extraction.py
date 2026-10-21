"""Manual extraction seam.

This module is the single, clearly-defined seam where raw transcript content is
turned into structured knowledge (Workflow, Problem, Adoption Risk, Stakeholder).
It is manual and structured by design: a future LLM-based extractor will be
substituted behind this same boundary without touching the rest of the model
(see ADR-0002).
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.deps import get_db

router = APIRouter()


def _get_meeting_or_404(db: Session, meeting_id: uuid.UUID) -> models.Meeting:
    meeting = db.get(models.Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


def _get_department_or_404(db: Session, department_id: uuid.UUID) -> models.Department:
    department = db.get(models.Department, department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# --- Workflow ---


@router.post(
    "/meetings/{meeting_id}/workflows",
    response_model=schemas.WorkflowRead,
    status_code=201,
)
def record_workflow(
    meeting_id: uuid.UUID,
    payload: schemas.WorkflowCreate,
    db: Session = Depends(get_db),
):
    meeting = _get_meeting_or_404(db, meeting_id)
    workflow = models.Workflow(
        description=payload.description,
        department_id=meeting.department_id,
        meeting_id=meeting_id,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


@router.get(
    "/departments/{department_id}/workflows",
    response_model=list[schemas.WorkflowRead],
)
def list_workflows(department_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_department_or_404(db, department_id)
    return db.scalars(
        select(models.Workflow).where(models.Workflow.department_id == department_id)
    ).all()


# --- Problem ---


@router.post(
    "/meetings/{meeting_id}/problems",
    response_model=schemas.ProblemRead,
    status_code=201,
)
def record_problem(
    meeting_id: uuid.UUID,
    payload: schemas.ProblemCreate,
    db: Session = Depends(get_db),
):
    meeting = _get_meeting_or_404(db, meeting_id)
    problem = models.Problem(
        title=payload.title,
        description=payload.description,
        workflow_id=payload.workflow_id,
        department_id=meeting.department_id,
        meeting_id=meeting_id,
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


@router.get(
    "/departments/{department_id}/problems",
    response_model=list[schemas.ProblemRead],
)
def list_problems(department_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_department_or_404(db, department_id)
    return db.scalars(
        select(models.Problem).where(models.Problem.department_id == department_id)
    ).all()


# --- Adoption Risk ---


@router.post(
    "/meetings/{meeting_id}/adoption-risks",
    response_model=schemas.AdoptionRiskRead,
    status_code=201,
)
def record_adoption_risk(
    meeting_id: uuid.UUID,
    payload: schemas.AdoptionRiskCreate,
    db: Session = Depends(get_db),
):
    meeting = _get_meeting_or_404(db, meeting_id)
    risk = models.AdoptionRisk(
        title=payload.title,
        description=payload.description,
        department_id=meeting.department_id,
        meeting_id=meeting_id,
    )
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk


@router.get(
    "/departments/{department_id}/adoption-risks",
    response_model=list[schemas.AdoptionRiskRead],
)
def list_adoption_risks(department_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_department_or_404(db, department_id)
    return db.scalars(
        select(models.AdoptionRisk).where(
            models.AdoptionRisk.department_id == department_id
        )
    ).all()


# --- Stakeholder ---


@router.post(
    "/departments/{department_id}/stakeholders",
    response_model=schemas.StakeholderRead,
    status_code=201,
)
def create_stakeholder(
    department_id: uuid.UUID,
    payload: schemas.StakeholderCreate,
    db: Session = Depends(get_db),
):
    _get_department_or_404(db, department_id)
    stakeholder = models.Stakeholder(
        name=payload.name, role=payload.role, department_id=department_id
    )
    db.add(stakeholder)
    db.commit()
    db.refresh(stakeholder)
    return stakeholder


@router.get(
    "/departments/{department_id}/stakeholders",
    response_model=list[schemas.StakeholderRead],
)
def list_department_stakeholders(department_id: uuid.UUID, db: Session = Depends(get_db)):
    _get_department_or_404(db, department_id)
    return db.scalars(
        select(models.Stakeholder).where(
            models.Stakeholder.department_id == department_id
        )
    ).all()


@router.post(
    "/meetings/{meeting_id}/stakeholders",
    response_model=schemas.StakeholderLink,
    status_code=201,
)
def link_stakeholder(
    meeting_id: uuid.UUID,
    payload: schemas.StakeholderLink,
    db: Session = Depends(get_db),
):
    meeting = _get_meeting_or_404(db, meeting_id)
    stakeholder = db.get(models.Stakeholder, payload.stakeholder_id)
    if stakeholder is None:
        raise HTTPException(status_code=404, detail="Stakeholder not found")
    if stakeholder not in meeting.stakeholders:
        meeting.stakeholders.append(stakeholder)
        db.commit()
    return payload


@router.get(
    "/meetings/{meeting_id}/stakeholders",
    response_model=list[schemas.StakeholderRead],
)
def list_meeting_stakeholders(meeting_id: uuid.UUID, db: Session = Depends(get_db)):
    meeting = _get_meeting_or_404(db, meeting_id)
    return meeting.stakeholders