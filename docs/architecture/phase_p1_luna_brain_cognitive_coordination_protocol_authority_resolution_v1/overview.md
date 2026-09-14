# Brain Cognitive Coordination Protocol Authority Resolution

This phase resolves the minimum authority model for four Brain-domain
coordination boundaries without creating a Brain runtime owner.

The result is intentionally partial. Existing owners are used where their
contracts establish mechanical or semantic authority; every remaining gap is
marked `OWNER_UNRESOLVED`.

Resolved boundaries:

- Cognitive Flow Governance owns candidate lifecycle mechanics and lifecycle
  state transitions.
- Cognitive State Formation Governance owns Sufficiency, Information Gap,
  Hypothesis Revision, and Stop production.
- Field Perception Orchestrator owns Re-observation execution/admission
  mechanics.
- Existing downstream Governance modules retain their own mutation authority.

Unresolved boundaries:

- Brain request admission;
- Goal/Concern to Information Need formation and registration;
- semantic Closure Acceptance;
- generic Assimilation Candidate routing/consumption.

No runtime component was changed in this phase.
