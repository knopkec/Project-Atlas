"""Hospital and Department API tests (ticket 02)."""

from tests.conftest import client

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def test_create_hospital():
    resp = client.post("/hospitals", json={"name": "Klinikum Südstadt"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Klinikum Südstadt"
    assert "id" in body


def test_list_hospitals():
    client.post("/hospitals", json={"name": "Klinikum Südstadt"})
    resp = client.get("/hospitals")
    assert resp.status_code == 200
    names = [h["name"] for h in resp.json()]
    assert "Klinikum Südstadt" in names


def test_get_hospital_by_id():
    created = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    resp = client.get(f"/hospitals/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Klinikum Südstadt"


def test_get_hospital_not_found():
    resp = client.get(f"/hospitals/{MISSING_ID}")
    assert resp.status_code == 404


def test_create_department():
    hospital = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    resp = client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": "Radiology Doctors"}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Radiology Doctors"
    assert body["hospital_id"] == hospital["id"]


def test_create_department_under_missing_hospital():
    resp = client.post(
        f"/hospitals/{MISSING_ID}/departments", json={"name": "Radiology Doctors"}
    )
    assert resp.status_code == 404


def test_list_departments():
    hospital = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": "Radiology Doctors"}
    )
    client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": "Radiology Nurses"}
    )
    resp = client.get(f"/hospitals/{hospital['id']}/departments")
    assert resp.status_code == 200
    names = [d["name"] for d in resp.json()]
    assert names == ["Radiology Doctors", "Radiology Nurses"]


def test_get_department_by_id():
    hospital = client.post("/hospitals", json={"name": "Klinikum Südstadt"}).json()
    created = client.post(
        f"/hospitals/{hospital['id']}/departments", json={"name": "Radiology Doctors"}
    ).json()
    resp = client.get(f"/departments/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Radiology Doctors"
