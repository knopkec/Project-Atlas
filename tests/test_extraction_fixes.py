"""Tests for extraction fixes: cross-department validation and read-by-id."""

from tests.conftest import client

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def _make_department(name):
    hospital = client.post("/hospitals", json={"name": f"H {name}"}).json()
    return client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": name}
    ).json()


def _make_meeting(dept):
    return client.post(
        f"/departments/{dept['id']}/meetings",
        json={"title": "Kickoff", "transcript": "raw"},
    ).json()


# --- Cross-department validation ---


def test_problem_cannot_reference_workflow_from_other_department():
    dept_a = _make_department("A")
    dept_b = _make_department("B")
    meeting_b = _make_meeting(dept_b)
    workflow_a = client.post(
        f"/meetings/{_make_meeting(dept_a)['id']}/workflows",
        json={"description": "in A"},
    ).json()
    resp = client.post(
        f"/meetings/{meeting_b['id']}/problems",
        json={"title": "x", "description": "y", "workflow_id": workflow_a["id"]},
    )
    assert resp.status_code == 404


def test_stakeholder_cannot_be_linked_to_meeting_in_other_department():
    dept_a = _make_department("A")
    dept_b = _make_department("B")
    meeting_b = _make_meeting(dept_b)
    stakeholder_a = client.post(
        f"/departments/{dept_a['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    ).json()
    resp = client.post(
        f"/meetings/{meeting_b['id']}/stakeholders",
        json={"stakeholder_id": stakeholder_a["id"]},
    )
    assert resp.status_code == 404


# --- Read-by-id for extracted entities ---


def test_get_workflow_by_id():
    dept = _make_department("A")
    meeting = _make_meeting(dept)
    created = client.post(
        f"/meetings/{meeting['id']}/workflows", json={"description": "process"}
    ).json()
    resp = client.get(f"/workflows/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["description"] == "process"


def test_get_problem_by_id():
    dept = _make_department("A")
    meeting = _make_meeting(dept)
    created = client.post(
        f"/meetings/{meeting['id']}/problems",
        json={"title": "slow", "description": "takes long"},
    ).json()
    resp = client.get(f"/problems/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "slow"


def test_get_adoption_risk_by_id():
    dept = _make_department("A")
    meeting = _make_meeting(dept)
    created = client.post(
        f"/meetings/{meeting['id']}/adoption-risks",
        json={"title": "no time", "description": "busy"},
    ).json()
    resp = client.get(f"/adoption-risks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "no time"


def test_get_stakeholder_by_id():
    dept = _make_department("A")
    created = client.post(
        f"/departments/{dept['id']}/stakeholders",
        json={"name": "Dr. Weber", "role": "Department head"},
    ).json()
    resp = client.get(f"/stakeholders/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Dr. Weber"
