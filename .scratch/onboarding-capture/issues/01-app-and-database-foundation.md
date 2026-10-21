# 01: App and database foundation

**What to build:** a running FastAPI application with a `/health` endpoint that responds successfully, backed by a local SQLite database and a working migration setup. This is the foundation every other ticket builds on.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] The app starts and serves a `/health` endpoint returning 200
- [ ] A local SQLite database is reachable (PostgreSQL + pgvector deferred to production, see ADR-0004)
- [ ] Migrations can be created and applied via Alembic
- [ ] The test harness runs a trivial smoke test against `/health`
