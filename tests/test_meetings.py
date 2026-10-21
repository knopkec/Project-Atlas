"""Meeting and transcript API tests (ticket 03)."""

from tests.conftest import client

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def _make_department(name="Radiology Doctors"):
    hospital = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    dept = client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": name}
    ).json()
    return dept


def test_create_meeting_with_transcript():
    dept = _make_department()
    resp = client.post(
        f"/departments/{dept['id']}/meetings",
        json={"title": "Kickoff", "transcript": "We discussed the current workflow."},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Kickoff"
    assert body["transcript"] == "We discussed the current workflow."
    assert body["department_id"] == dept["id"]


def test_create_meeting_under_missing_department():
    resp = client.post(
        f"/departments/{MISSING_ID}/meetings",
        json={"title": "Kickoff", "transcript": "..."},
    )
    assert resp.status_code == 404


def test_list_meetings_for_department():
    dept = _make_department()
    client.post(
        f"/departments/{dept['id']}/meetings", json={"title": "Kickoff", "transcript": "a"}
    )
    client.post(
        f"/departments/{dept['id']}/meetings", json={"title": "Follow-up", "transcript": "b"}
    )
    resp = client.get(f"/departments/{dept['id']}/meetings")
    assert resp.status_code == 200
    titles = [m["title"] for m in resp.json()]
    assert titles == ["Kickoff", "Follow-up"]


def test_list_meetings_for_missing_department():
    resp = client.get(f"/departments/{MISSING_ID}/meetings")
    assert resp.status_code == 404


def test_get_meeting_by_id():
    dept = _make_department()
    created = client.post(
        f"/departments/{dept['id']}/meetings",
        json={"title": "Kickoff", "transcript": "full transcript here"},
    ).json()
    resp = client.get(f"/meetings/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["transcript"] == "full transcript here"
