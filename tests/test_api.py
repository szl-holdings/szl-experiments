from fastapi.testclient import TestClient

from app import app


def test_health_and_allodial() -> None:
    c = TestClient(app)
    h = c.get("/health")
    assert h.status_code == 200
    assert h.json()["locked_eight_unchanged"] is True
    score = c.get("/api/experiments/v1/allodial/score", params={"seals": "4,4,4,4,4", "dep": "0"})
    assert score.status_code == 200
    assert score.json()["posture"] == "allodial"


def test_chamber() -> None:
    c = TestClient(app)
    page = c.get("/")
    assert page.status_code == 200
    assert "Experiments lab" in page.text
