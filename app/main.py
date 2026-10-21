"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="OWC Consultant Copilot")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
