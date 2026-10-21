# OWC Consultant Copilot

Assists OWC's implementation consultants during hospital onboarding and rollout. OWC is a consultancy that helps hospitals stand up their own local AI server; the server ships with two software programs — Schreibdienst (voice-to-text transcription) and Curaflow (work-schedule planning). The software is open core; the customer pays for the service: integration, adaptation, training, and maintenance. The copilot's job is to capture that implementation knowledge and reuse it across projects — not customer support.

## Language

### Organizations and people

**Hospital**:
A healthcare organization whose departments are onboarded onto the product. The pilot is Klinikum Südstadt; more departments and more hospitals follow later.
_Avoid_: Customer, Client, Site, Account

**Department**:
The unit of integration: a group within a hospital that runs its processes in its own way (e.g. radiology doctors, radiology nurses). Each department is onboarded, configured, and measured independently.
_Avoid_: Unit, Team, Ward, Group

**Stakeholder**:
A person involved in a department's rollout — a department head, clinician, or IT contact — who attends meetings and speaks for their side.
_Avoid_: User, Contact, Attendee, Person

### Capture

**Meeting**:
An onboarding or rollout session with a department, captured as a transcript. Includes training sessions.
_Avoid_: Session, Interview, Call, Appointment

**Transcript**:
The captured text of a meeting; the raw source from which workflows, problems, and risks are extracted.
_Avoid_: Notes, Minutes, Recording

### The deliverable

**Local AI Server**:
The on-premises AI server OWC installs at a hospital; the infrastructure Schreibdienst and Curaflow run on. One per hospital, shared across its departments; departments integrate on top of it independently.
_Avoid_: Server, Instance, Host

**Software**:
One of the programs OWC ships with the local AI server — Schreibdienst or Curaflow. A first-class entity that Configurations adapt and Lessons reference.
_Avoid_: Tool, App, Module

**Schreibdienst**:
OWC's voice-to-text transcription software, ship before OWC arrives — a legacy transcription or scheduling tool, for example — distinct from what OWC delivers
_Avoid_: Transcription tool, Voice-to-text

**Curaflow**:
OWC's work-schedule planning software, shipped with the local AI server.
_Avoid_: Scheduling tool, Roster planner

### Current state

**Workflow**:
A department's current (as-is) way of doing a process before the rollout. Future-state changes are expressed only in Recommendations and Configurations, never a second target workflow.
_Avoid_: Process, Current state

**Existing Software**:
Software the hospital or department already uses, distinct from the product being rolled out.
_Avoid_: Legacy system, Current system

**Problem**:
A shortcoming in a department's current workflow that the rollout solves for the department head. Interchangeable with pain point; resolved by a Recommendation.
_Avoid_: Issue, Ticket, Bug, Concern

**Adoption Risk**:
A reason a department resists switching despite the improvement (e.g. no time to learn new software). A barrier to change, not a flaw in the current workflow; mitigated by change management, not a workflow change.
_Avoid_: Blocker, Obstacle, Resistance

### Future state

**Recommendation**:
A project-specific, actionable suggestion tied to one Problem at one department.
_Avoid_: Advice, Suggestion, Action item

**Configuration**:
The integration and adaptation of the local AI server, Schreibdienst, and/or Curaflow to a department's rollout; the future-state counterpart to a department's Workflow.
_Avoid_: Setting, Setup, Customization

### Reuse

**Lesson Learned**:
A generalized, reusable distillation of experience across projects: a pattern of characteristic → problem → approach. Feeds cross-hospital semantic search.
_Avoid_: Insight, Takeaway, Best practice
