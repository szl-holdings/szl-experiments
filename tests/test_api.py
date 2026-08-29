from fastapi.testclient import TestClient

from app import app


c = TestClient(app)


def test_health_mounts_research_tabs() -> None:
    h = c.get("/health")
    assert h.status_code == 200
    body = h.json()
    assert body["locked_eight_unchanged"] is True
    mounted = set(body["mounted"])
    for name in (
        "allodial", "neuroplasticity", "chain-of-title",
        "entanglement", "scaling", "sapa", "restraint",
    ):
        assert name in mounted, (name, body.get("mount_errors"))


def test_chamber_lists_missing_tabs() -> None:
    page = c.get("/")
    assert page.status_code == 200
    text = page.text
    assert "Entanglement" in text
    assert "Metabolic scaling" in text
    assert "SAPA" in text
    assert "Restraint" in text


def test_entangle_and_kleiber() -> None:
    bell = c.get("/api/experiments/v1/entangle/concurrence", params={"state": "bell"})
    assert bell.status_code == 200
    assert abs(bell.json()["concurrence"] - 1.0) < 1e-5
    k = c.get("/api/experiments/v1/scaling/kleiber", params={"M": "70"})
    assert k.status_code == 200
    assert 1500 < k.json()["B_kcal_day"] < 1900


def test_allodial_still_works() -> None:
    score = c.get("/api/experiments/v1/allodial/score", params={"seals": "4,4,4,4,4", "dep": "0"})
    assert score.status_code == 200
    assert score.json()["posture"] == "allodial"


def test_index_names_restored() -> None:
    idx = c.get("/api/v1/experiments/index")
    assert idx.status_code == 200
    body = idx.json()
    ids = {t["id"] for t in body["research_experimental_tabs"]}
    assert ids == {"neuro", "sovereignty", "allodialai", "l6chain", "entangle", "scaling"}
    restored = {t["id"] for t in body["restored_deleted_tabs"]}
    assert restored == {"restraint", "sapa"}
