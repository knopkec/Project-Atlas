# Department is the unit of integration

A hospital (e.g. Klinikum Südstadt) contains multiple departments, each of which runs its processes in its own way and is onboarded independently. We treat **Department** — not Hospital, and not a separate Implementation/Engagement entity — as the unit of integration that owns workflows, problems, configurations, and meetings. Chosen because each department integrates separately, so a hospital-level or a separate "implementation" aggregate would duplicate the department's role until a hospital actually runs two concurrent rollouts. Revisit only when that happens.

Nuance: the **local AI server is one per hospital** (shared infrastructure); what varies per department is the integration layered on top of it — its workflows, configurations, problems, and meetings. So Department remains the integration unit even though the server is hospital-scoped.
