"""Hospital and Department routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.deps import get_db

router = APIRouter()


@router.post("/hospitals", response_model=schemas.HospitalRead, status_code=201)
def create_hospital(payload: schemas.HospitalCreate, db: Session = Depends(get_db)):
    hospital = models.Hospital(name=payload.name)
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


@router.get("/hospitals", response_model=list[schemas.HospitalRead])
def list_hospitals(db: Session = Depends(get_db)):
    return db.scalars(select(models.Hospital)).all()


@router.get("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def get_hospital(hospital_id: uuid.UUID, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.post(
    "/hospitals/{hospital_id}/departments",
    response_model=schemas.DepartmentRead,
    status_code=201,
)
def create_department(
    hospital_id: uuid.UUID,
    payload: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
):
    if db.get(models.Hospital, hospital_id) is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    department = models.Department(name=payload.name, hospital_id=hospital_id)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.get(
    "/hospitals/{hospital_id}/departments",
    response_model=list[schemas.DepartmentRead],
)
def list_departments(hospital_id: uuid.UUID, db: Session = Depends(get_db)):
    if db.get(models.Hospital, hospital_id) is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db.scalars(
        select(models.Department).where(models.Department.hospital_id == hospital_id)
    ).all()


@router.get("/departments/{department_id}", response_model=schemas.DepartmentRead)
def get_department(department_id: uuid.UUID, db: Session = Depends(get_db)):
    department = db.get(models.Department, department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.post(
    "/departments/{department_id}/meetings",
    response_model=schemas.MeetingRead,
    status_code=201,
)
def create_meeting(
    department_id: uuid.UUID,
    payload: schemas.MeetingCreate,
    db: Session = Depends(get_db),
):
    if db.get(models.Department, department_id) is None:
        raise HTTPException(status_code=404, detail="Department not found")
    meeting = models.Meeting(
        title=payload.title, transcript=payload.transcript, department_id=department_id
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get(
    "/departments/{department_id}/meetings",
    response_model=list[schemas.MeetingRead],
)
def list_meetings(department_id: uuid.UUID, db: Session = Depends(get_db)):
    if db.get(models.Department, department_id) is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db.scalars(
        select(models.Meeting).where(models.Meeting.department_id == department_id)
    ).all()


@router.get("/meetings/{meeting_id}", response_model=schemas.MeetingRead)
def get_meeting(meeting_id: uuid.UUID, db: Session = Depends(get_db)):
    meeting = db.get(models.Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
