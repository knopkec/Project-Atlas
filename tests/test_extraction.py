"""Manual extraction API tests (ticket 04): Workflow, Problem, Stakeholder, Adoption Risk."""

from tests.conftest import client

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def _make_meeting():
    hospital = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    dept = client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": "Radiology Doctors"}
    ).json()
    meeting = client.post(
        f"/departments/{dept['id']}/meetings",
        json={"title": "Kickoff", "transcript": "raw transcript"},
    ).json()
    return dept, meeting


# --- Workflow ---


def test_record_workflow_against_meeting():
    dept, meeting = _make_meeting()
    resp = client.post(
        f"/meetings/{meeting['id']}/workflows",
        json={"description": "Images are reported by a radiologist then typed up."},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["description"] == "Images are reported by a radiologist then typed up."
    assert body["meeting_id"] == meeting["id"]
    assert body["department_id"] == dept["id"]


def test_workflow_against_missing_meeting_fails():
    resp = client.post(
        f"/meetings/{MISSING_ID}/workflows", json={"description": "x"}
    )
    assert resp.status_code == 404


def test_list_department_workflows():
    dept, meeting = _make_meeting()
    client.post(
        f"/meetings/{meeting['id']}/workflows", json={"description": "process one"}
    )
    resp = client.get(f"/departments/{dept['id']}/workflows")
    assert resp.status_code == 200
    assert [w["description"] for w in resp.json()] == ["process one"]


# --- Problem ---


def test_record_problem_against_meeting():
    dept, meeting = _make_meeting()
    workflow = client.post(
        f"/meetings/{meeting['id']}/workflows",
        json={"description": "reporting is manual"},
    ).json()
    resp = client.post(
        f"/meetings/{meeting['id']}/problems",
        json={
            "title": "Manual reporting is slow",
            "description": "Typing up reports takes too long.",
            "workflow_id": workflow["id"],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Manual reporting is slow"
    assert body["workflow_id"] == workflow["id"]
    assert body["meeting_id"] == meeting["id"]
    assert body["department_id"] == dept["id"]


def test_problem_against_missing_meeting_fails():
    resp = client.post(
        f"/meetings/{MISSING_ID}/problems",
        json={"title": "x", "description": "y"},
    )
    assert resp.status_code == 404


def test_list_department_problems():
    dept, meeting = _make_meeting()
    client.post(
        f"/meetings/{meeting['id']}/problems",
        json={"title": "Slow reporting", "description": "takes too long"},
    )
    resp = client.get(f"/departments/{dept['id']}/problems")
    assert resp.status_code == 200
    assert [p["title"] for p in resp.json()] == ["Slow reporting"]


# --- Adoption Risk ---


def test_record_adoption_risk_against_meeting():
    dept, meeting = _make_meeting()
    resp = client.post(
        f"/meetings/{meeting['id']}/adoption-risks",
        json={"title": "No time to learn", "description": "Staff are overbooked."},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "No time to learn"
    assert body["meeting_id"] == meeting["id"]
    assert body["department_id"] == dept["id"]


def test_adoption_risk_against_missing_meeting_fails():
    resp = client.post(
        f"/meetings/{MISSING_ID}/adoption-risks",
        json={"title": "x", "description": "y"},
    )
    assert resp.status_code == 404


# --- Stakeholder ---


def test_create_reusable_stakeholder():
    dept, _ = _make_meeting()
    resp = client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Dr. Weber"
    assert body["role"] == "Department head"
    assert body["department_id"] == dept["id"]


def test_link_stakeholder_to_meeting():
    dept, meeting = _make_meeting()
    stakeholder = client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    ).json()
    resp = client.post(
        f"/meetings/{meeting['id']}/stakeholders",
        json={"stakeholder_id": stakeholder["id"]},
    )
    assert resp.status_code == 201
    assert resp.json()["stakeholder_id"] == stakeholder["id"]


def test_link_stakeholder_to_missing_meeting_fails():
    resp = client.post(
        f"/meetings/{MISSING_ID}/stakeholders",
        json={"stakeholder_id": MISSING_ID},
    )
    assert resp.status_code == 404


def test_list_meeting_stakeholders():
    dept, meeting = _make_meeting()
    s = client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    ).json()
    client.post(
        f"/meetings/{meeting['id']}/stakeholders", json={"stakeholder_id": s["id"]}
    )
    resp = client.get(f"/meetings/{meeting['id']}/stakeholders")
    assert resp.status_code == 200
    names = [x["name"] for x in resp.json()]
    assert names == ["Dr. Weber"]


def test_list_department_stakeholders():
    dept, _ = _make_meeting()
    client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    )
    client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "N. Klein", "role": "Nurse"},
    )
    resp = client.get(f"/departments/{dept['id']}/stakeholders")
    assert resp.status_code == 200
    assert [s["name"] for s in resp.json()] == ["Dr. Weber", "N. Klein"]
