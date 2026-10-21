"""FastAPI application entry point."""

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import extraction, hospitals

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI(title="OWC Consultant Copilot")
app.include_router(hospitals.router)
app.include_router(extraction.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
