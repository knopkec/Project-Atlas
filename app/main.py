"""FastAPI application entry point."""

from fastapi import FastAPI

from app.routers import hospitals

app = FastAPI(title="OWC Consultant Copilot")
app.include_router(hospitals.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
