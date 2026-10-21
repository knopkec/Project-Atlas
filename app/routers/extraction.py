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


def _get_or_404(db: Session, model, entity_id: uuid.UUID, label: str):
    entity = db.get(model, entity_id)
    if entity is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return entity


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
    if payload.workflow_id is not None:
        workflow = _get_or_404(db, models.Workflow, payload.workflow_id, "Workflow")
        if workflow.department_id != meeting.department_id:
            raise HTTPException(
                status_code=404, detail="Workflow not found for this department"
            )
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
    stakeholder = _get_or_404(db, models.Stakeholder, payload.stakeholder_id, "Stakeholder")
    if stakeholder.department_id != meeting.department_id:
        raise HTTPException(
            status_code=404, detail="Stakeholder not found for this department"
        )
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


# --- Read-by-id ---


@router.get("/workflows/{workflow_id}", response_model=schemas.WorkflowRead)
def get_workflow(workflow_id: uuid.UUID, db: Session = Depends(get_db)):
    return _get_or_404(db, models.Workflow, workflow_id, "Workflow")


@router.get("/problems/{problem_id}", response_model=schemas.ProblemRead)
def get_problem(problem_id: uuid.UUID, db: Session = Depends(get_db)):
    return _get_or_404(db, models.Problem, problem_id, "Problem")


@router.get("/adoption-risks/{risk_id}", response_model=schemas.AdoptionRiskRead)
def get_adoption_risk(risk_id: uuid.UUID, db: Session = Depends(get_db)):
    return _get_or_404(db, models.AdoptionRisk, risk_id, "Adoption risk")


@router.get("/stakeholders/{stakeholder_id}", response_model=schemas.StakeholderRead)
def get_stakeholder(stakeholder_id: uuid.UUID, db: Session = Depends(get_db)):
    return _get_or_404(db, models.Stakeholder, stakeholder_id, "Stakeholder")