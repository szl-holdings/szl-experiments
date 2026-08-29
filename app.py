"""SZL Experiments — operational experimental tier.

Allodial AI, neuroplasticity, chain-of-title. EXPERIMENTAL, not locked-8.
Λ = Conjecture 1. Never folded into the eight proven formulas.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "formulas"))

import szl_allodial as allodial  # noqa: E402
import szl_chain_of_title as chain  # noqa: E402
import szl_neuroplasticity as neuro  # noqa: E402

CHAMBER = ROOT / "static" / "chamber.html"
LOCKED_EIGHT = ["F1", "F4", "F7", "F11", "F12", "F18", "F19", "F22"]

app = FastAPI(
    title="SZL Experiments",
    version="1.0.0",
    description="Operational experimental tier. Not locked-8. Λ = Conjecture 1.",
)

allodial.register(app, ns="experiments")
neuro.register(app, ns="experiments")
chain.register(app, ns="experiments")


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "product": "SZL Experiments",
        "tier": "EXPERIMENTAL",
        "locked_eight_unchanged": True,
        "locked_eight": LOCKED_EIGHT,
        "lambda": "CONJECTURE_1",
        "surfaces": ["allodial", "neuroplasticity", "chain-of-title"],
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
    return {
        "schema": "szl.experiments.index/v1",
        "tier": "EXPERIMENTAL · CI-green · NOT in locked-8",
        "lambda": "CONJECTURE_1",
        "locked_eight_unchanged": True,
        "labs": [
            {
                "id": "allodial",
                "name": "Allodial AI",
                "routes": "/api/experiments/v1/allodial/*",
                "honesty": "PROPOSED engineering gate. Not a theorem. Not above the law.",
            },
            {
                "id": "neuroplasticity",
                "name": "Neuroplasticity",
                "routes": "/api/experiments/v1/neuro/*",
                "honesty": "Cited learning rules, runnable. Not a claim that Λ learns.",
            },
            {
                "id": "chain-of-title",
                "name": "Chain of title L6",
                "routes": "/api/experiments/v1/chain/*",
                "honesty": "Assembles receipt STRUCTURE. Does not fabricate signatures.",
            },
        ],
    }


@app.get("/api/v1/experiments/selftest")
def selftest() -> JSONResponse:
    errors: list[str] = []
    try:
        allodial._selftest()
    except Exception as exc:
        errors.append(f"allodial: {exc}")
    try:
        neuro._selftest()
    except Exception as exc:
        errors.append(f"neuro: {exc}")
    return JSONResponse(
        {
            "ok": not errors,
            "errors": errors,
            "lambda": "CONJECTURE_1",
            "tier": "EXPERIMENTAL",
        },
        status_code=200 if not errors else 500,
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8100"))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
