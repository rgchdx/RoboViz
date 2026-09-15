# FastAPI application entrypoint for the RoboViz API. This basically sets up the app, middleware, and routes.
"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chain_routes import router as chain_router
from app.api.jacobian_routes import router as jacobian_router
from app.api.routes import router as kinematics_router

app = FastAPI(title="RoboViz API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kinematics_router, prefix="/api")
app.include_router(jacobian_router, prefix="/api")
app.include_router(chain_router, prefix="/api")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
