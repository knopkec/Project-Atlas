# OWC Consultant Copilot — Onboarding Capture (thin slice)

## Problem Statement

OWC consultants capture implementation knowledge during hospital onboarding, but today that knowledge lives in heads and scattered notes. When a new department or hospital begins onboarding, there's no reliable way to recall how a similar department was handled before. The consultant can't answer "how was this handled elsewhere?" without asking a colleague or digging through old documents.

## Solution

A consultant-copilot tool that captures the core of an onboarding engagement as structured, reusable data. In this first slice, a consultant records a hospital, its departments, the meetings they hold, the meeting transcripts, and the knowledge extracted from each meeting (workflow, problems, stakeholders, adoption risks). Every layer is reachable through a FastAPI JSON API, so a future UI and a future AI-consultant can both be built on the same boundary.

## User Stories

1. As a consultant, I want to create a hospital (e.g. Klinikum Südstadt), so that I can start capturing an onboarding engagement.
2. As a consultant, I want to create departments under a hospital (e.g. radiology doctors, radiology nurses), so that I can track each integration unit separately, since each department runs its processes differently.
3. As a consultant, I want to list a hospital's departments, so that I can see which units are being onboarded.
4. As a consultant, I want to record a meeting for a department, so that I can log when onboarding discussions happen.
5. As a consultant, I want to attach a transcript to a meeting, so that the raw source of the discussion is preserved.
6. As a consultant, I want to list a department's meetings, so that I can review what has been discussed with that unit.
7. As a consultant, I want to record the current workflow extracted from a meeting, so that the as-is process is captured.
8. As a consultant, I want to record problems (pain points) from a meeting, so that I capture what the rollout must solve for the department head.
9. As a consultant, I want to record adoption risks from a meeting, so that I capture why a department might resist switching.
10. As a consultant, I want to record stakeholders from a meeting, so that I know who speaks for which side of the rollout.
11. As a consultant, I want extracted items to stay linked to the meeting they came from, so that I can trace any item back to its source.
12. As a consultant, I want extracted items to stay linked to their department, so that I can see everything known about one unit.

## Implementation Decisions

- **Tech stack**: FastAPI backend, Pydantic models, Alembic for migrations, SQLAlchemy. The prototype stores data in local SQLite (see ADR-0004); PostgreSQL with pgvector is the production target, reached by setting `DATABASE_URL`.
- **One seam for testing**: the HTTP API. Tests cross the seam with FastAPI's test client and assert external behaviour only. Unit tests are reserved for behaviour not reachable over HTTP.
- **The Department is the integration unit**: workflows, meetings, problems, stakeholders, and adoption risks all belong to a Department; a Hospital contains many Departments. (See ADR-0001.)
- **Extraction is manual and structured, behind a seam**: the prototype accepts structured, human-entered extraction results. The extraction is exposed as a clearly-defined boundary so a future LLM extractor can be substituted without touching the rest of the model. (See ADR-0002.)
- **Entities in this slice**: Hospital, Department, Meeting, Transcript, Workflow, Problem, Stakeholder, Adoption Risk. Software, Local AI Server, Existing Software, Recommendation, Configuration, and Lesson Learned are out of scope for this slice.
- **Identifiers**: every entity has a stable unique identifier returned by the API, used by clients and by future slices to link entities.
- **Keep it simple, avoid premature optimisation**: no caching, no background jobs, no auth in this slice. Synchronous SQL via a thin data-access layer is sufficient.

## Testing Decisions

- A good test asserts **external behaviour** (status codes, response shapes, the resulting list/read state) and never internal class or table details.
- Tests cross the **HTTP seam** using the FastAPI test client against a test database.
- Every route gets at least one happy-path test and one validation/not-found test.
- Prior art: none in this repo yet — these tests set the pattern.

## Out of Scope

- Semantic search and pgvector embeddings (ADR-0003; a later slice).
- Generation of implementation summaries, workflow diagrams, or rollout recommendations.
- Recommendation, Configuration, and Lesson Learned entities.
- Software, Local AI Server, and Existing Software entities.
- AI/LLM-based extraction (the seam is left open for it, but it is not built here).
- Authentication and multi-tenant authorisation.
- A user interface (the API is the deliverable for this slice).

## Further Notes

This is the first vertical slice of the OWC Consultant Copilot. It deliberately keeps the capture core small so the domain model can be validated against real usage before search, generation, and reuse features are layered on. The full model and its rationale live in `GLOSSARY.md` and `docs/adr/`.
