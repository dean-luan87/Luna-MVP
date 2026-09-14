# Capability Task Router Overlap v1

`task_manager_capability_router_v1.py` currently loads the capability registry,
maps requested capability IDs to module API refs, derives lifecycle-based
routing status and emits execution request candidates/blockers.

Classification:

- requirement extraction: retain in Task only for Task functional needs;
- registry lookup: compatibility overlap; target Capability Registry/Governance;
- module routing: reassign to Capability scope/resolution;
- Provider identity: must not be owned by Task; Provider Governance;
- execution request candidate: retain only as a governed handoff ref;
- blocker handling: preserve source blocker, but owner-specific failure remains
  Capability/Model/Diagnostics/Provider.

Disposition: NARROW / COMPATIBILITY_ONLY. No deletion or migration occurs in
this phase.
