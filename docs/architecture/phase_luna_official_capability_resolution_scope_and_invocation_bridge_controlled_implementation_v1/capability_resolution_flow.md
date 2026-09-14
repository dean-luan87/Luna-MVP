# Capability Resolution Flow

The scoped path is ordered as:

`Requirement → Module discovery → Scope Assessment → admission/lifecycle →
Slot binding → health → resource → permission → compatibility → dependency
references → READY/UNAVAILABLE/DEGRADED candidate`.

The existing readiness vocabulary is reused. Scope failure produces explicit
unavailable resolution and optional Gap Candidate; no fallback hallucination.
