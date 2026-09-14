# Intent / Cognitive Loop Boundary v1

Loop may persist `intent_ref`, `intent_version_ref`, applicability/status
refs, supersession refs, handoff refs and trace/provenance. It may reject a
mechanical command for wrong scope, stale version, revoked grant or invalid
transition.

Loop must not infer that an Intent is suspended, resumed, superseded or
closed. Intent Governance supplies the semantic lifecycle decision; Brain may
supply global constraints; Loop records the authorized mechanical consequence.

An Intent change can invalidate a Loop's envelope or require a supplied
pause/resume/supersede command. It cannot directly command Loop persistence
without the existing governed mechanical adapter.
