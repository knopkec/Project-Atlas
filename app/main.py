"""FastAPI application entry point."""

from fastapi import FastAPI

from app.routers import extraction, hospitals

app = FastAPI(title="OWC Consultant Copilot")
app.include_router(hospitals.router)
app.include_router(extraction.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
