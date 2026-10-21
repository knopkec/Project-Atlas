# 01: App and database foundation

**What to build:** a running FastAPI application with a `/health` endpoint that responds successfully, backed by a PostgreSQL database with the pgvector extension enabled and a working migration setup. This is the foundation every other ticket builds on.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] The app starts and serves a `/health` endpoint returning 200
- [ ] PostgreSQL is reachable and the pgvector extension is enabled
- [ ] Migrations can be created and applied via Alembic
- [ ] The test harness runs a trivial smoke test against `/health`
