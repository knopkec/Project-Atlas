# 04: Manual extraction

**What to build:** the ability to record extracted knowledge against a meeting — a workflow, problems, stakeholders, and adoption risks — each linked to the meeting it came from and the department that owns it, all exposed behind a clearly-defined extraction seam.

**Blocked by:** 03 (Meeting with transcript)

**Status:** ready-for-agent

- [ ] A workflow can be recorded against a meeting and read back
- [ ] A problem can be recorded against a meeting and read back
- [ ] A stakeholder can be recorded against a meeting and read back
- [ ] An adoption risk can be recorded against a meeting and read back
- [ ] Each extracted item links to its meeting and its department
- [ ] The extraction boundary is a clearly-defined seam (no LLM; a future extractor can be swapped in)
- [ ] Recording an extraction against a non-existent meeting fails cleanly
