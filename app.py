"""SZL Experiments — every a-11-oy.com experimental / deleted research tab.

Research (Experimental) nav from a11oy_nav_wireup.py:
  neuro, sovereignty/allodial, allodialai, l6chain, entangle, scaling

Deleted from console nav because they were SPA shells:
  /restraint  (real ladder is here)
  /sapa       (joules-per-successful-goal; UNAVAILABLE without a meter)

Plus the other EXPERIMENTAL formula organs that lived beside those tabs:
  unified, cuas (effector SIMULATED), neuromorphic, qbio, conjecture-factory.

Never folded into locked-8. Λ = Conjecture 1.
"""
from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "formulas"))

CHAMBER = ROOT / "static" / "chamber.html"
LOCKED_EIGHT = ["F1", "F4", "F7", "F11", "F12", "F18", "F19", "F22"]

app = FastAPI(
    title="SZL Experiments",
    version="1.1.0",
    description="Operational experimental + restored tabs. Not locked-8. Λ = Conjecture 1.",
)

MOUNTED: list[str] = []
MOUNT_ERRORS: dict[str, str] = {}


def _mount(name: str, fn) -> None:
    try:
        fn()
        MOUNTED.append(name)
    except Exception as exc:
        MOUNT_ERRORS[name] = f"{type(exc).__name__}: {exc}"[:240]


def _reg_allodial() -> None:
    import szl_allodial as m
    m.register(app, ns="experiments")


def _reg_neuro() -> None:
    import szl_neuroplasticity as m
    m.register(app, ns="experiments")


def _reg_chain() -> None:
    import szl_chain_of_title as m
    m.register(app, ns="experiments")


def _reg_entangle() -> None:
    import szl_entanglement as m
    m.register(app, ns="experiments")


def _reg_scaling() -> None:
    import szl_scaling as m
    m.register(app, ns="experiments")


def _reg_unified() -> None:
    import szl_unified_formulas as m
    m.register(app, ns="experiments")


def _reg_cuas() -> None:
    import szl_cuas_formulas as m
    m.register(app, ns="experiments")


def _reg_neuro_morph() -> None:
    import szl_neuromorphic as m
    m.register(app, ns="experiments")


def _reg_qbio() -> None:
    import szl_quantum_bio as m
    m.register(app, ns="experiments")


def _reg_restraint() -> None:
    import szl_restraint as m
    m.register(app, ns="experiments")


def _reg_conjecture() -> None:
    import szl_conjecture_factory as m
    m.register(app, ns="experiments")


_mount("allodial", _reg_allodial)
_mount("neuroplasticity", _reg_neuro)
_mount("chain-of-title", _reg_chain)
_mount("entanglement", _reg_entangle)
_mount("scaling", _reg_scaling)
_mount("unified", _reg_unified)
_mount("cuas", _reg_cuas)
_mount("neuromorphic", _reg_neuro_morph)
_mount("qbio", _reg_qbio)
_mount("restraint", _reg_restraint)
_mount("conjecture-factory", _reg_conjecture)

# SAPA never had register() — the /sapa tab was deleted because it fell through
# to the SPA shell. Restore the real accounting function as an honest endpoint.
try:
    import szl_sapa as sapa

    @app.get("/api/experiments/v1/sapa/summary")
    def sapa_summary() -> dict:
        snap = sapa.compute_sapa()
        snap["restored_tab"] = "/sapa was excluded from console nav (SPA shell only)"
        snap["honesty"] = (
            "MEASURED only when a live joule meter + completed trajectories exist; "
            "otherwise UNAVAILABLE. Never fabricates joules."
        )
        return snap

    @app.get("/api/experiments/v1/sapa/receipt")
    def sapa_receipt() -> dict:
        return sapa.sapa_receipt()

    MOUNTED.append("sapa")
except Exception as exc:
    MOUNT_ERRORS["sapa"] = f"{type(exc).__name__}: {exc}"[:240]


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "product": "SZL Experiments",
        "version": "1.1.0",
        "tier": "EXPERIMENTAL",
        "locked_eight_unchanged": True,
        "locked_eight": LOCKED_EIGHT,
        "lambda": "CONJECTURE_1",
        "mounted": MOUNTED,
        "mount_errors": MOUNT_ERRORS,
        "origins": {
            "product": "https://a-11-oy.com",
            "proof": "https://a11oy.net",
            "github": "https://github.com/szl-holdings/szl-experiments",
            "space": "https://huggingface.co/spaces/SZLHOLDINGS/experiments",
        },
    }


@app.get("/", response_class=HTMLResponse)
def chamber() -> HTMLResponse:
    return HTMLResponse(CHAMBER.read_text(encoding="utf-8"))


@app.get("/api/v1/experiments/index")
def index() -> dict:
    try:
        from experimental_tier import handle_experimental_index
        tier = handle_experimental_index()
    except Exception as exc:
        tier = {"status": "UNAVAILABLE", "honesty": str(exc)[:160]}
    return {
        "schema": "szl.experiments.index/v2",
        "tier": "EXPERIMENTAL · NOT in locked-8",
        "lambda": "CONJECTURE_1",
        "locked_eight_unchanged": True,
        "mounted": MOUNTED,
        "research_experimental_tabs": [
            {"id": "neuro", "name": "Neuroplasticity", "status": "LIVE_SOFTWARE"},
            {"id": "sovereignty", "name": "Sovereignty (Allodial)", "status": "LIVE_SOFTWARE"},
            {"id": "allodialai", "name": "Allodial AI", "status": "LIVE_SOFTWARE"},
            {"id": "l6chain", "name": "Chain of Title", "status": "LIVE_SOFTWARE"},
            {"id": "entangle", "name": "Entanglement", "status": "LIVE_SOFTWARE"},
            {"id": "scaling", "name": "Metabolic Scaling", "status": "LIVE_SOFTWARE"},
        ],
        "restored_deleted_tabs": [
            {
                "id": "restraint",
                "was": "/restraint — excluded from console nav (SPA catch-all shell)",
                "now": "/api/experiments/v1/restraint/* and /restraint-bench on product",
            },
            {
                "id": "sapa",
                "was": "/sapa — excluded from console nav (no dedicated page)",
                "now": "/api/experiments/v1/sapa/summary — joules/successful-goal, fail-closed",
            },
        ],
        "additional_experimental_organs": [
            "unified", "cuas (effector SIMULATED)", "neuromorphic",
            "qbio", "conjecture-factory",
        ],
        "experimental_tier": tier,
    }


@app.get("/api/v1/experiments/selftest")
def selftest() -> JSONResponse:
    errors: list[str] = []
    for name, mod in (
        ("allodial", "szl_allodial"),
        ("neuro", "szl_neuroplasticity"),
        ("entangle", "szl_entanglement"),
        ("scaling", "szl_scaling"),
        ("unified", "szl_unified_formulas"),
        ("cuas", "szl_cuas_formulas"),
        ("chain", "szl_chain_of_title"),
    ):
        try:
            m = __import__(mod)
            m._selftest()
        except Exception as exc:
            errors.append(f"{name}: {exc}")
            traceback.print_exc()
    return JSONResponse(
        {
            "ok": not errors,
            "errors": errors,
            "mounted": MOUNTED,
            "lambda": "CONJECTURE_1",
            "tier": "EXPERIMENTAL",
        },
        status_code=200 if not errors else 500,
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8100"))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
