# M07 Intent Governance — Module Review

## Identity and purpose

Canonical name: Intent Governance. Evidence: `capabilities/midplatform/core/intent_governance/intent_governance_skeleton_v1.py`, `intent_ownership_guard_v1.py`, `intent_core_types_v1.py`, and `intent_registry_v1.py`. If removed, Luna loses ownership, validation, and controlled handoff of Intent candidates.

## Functions and authority

`CORE`: construct/validate Intent and Potential Intent candidates, preserve owner/provenance, issue governed causal handoff. `SUPPORTING`: lifecycle/IO/static guards. Outputs are candidate/governance refs; it does not own A Need, Task completion, World Truth, Action, or Loop mechanics. `INTENT_OWNER` is the source owner; causal handoff recipient is separately named. Responsibility is intent provenance/ownership correctness.

## Inputs, outputs, state, lifecycle

Inputs: intent requests, source refs, causal context, provenance; outputs: Intent/PotentialIntent and handoff candidates. State is authoritative within Intent Governance only if/when a runtime owner exists; current implementation is candidate/skeleton. Lifecycle: request → validate → candidate → handoff/accept/reject/defer → supersede/archive.

## Communication and negative boundaries

Allowed: upstream governance/user/task context→Intent Governance; Intent→Causal/A context and A envelope. Forbidden: arbitrary modules mutating Intent, Intent→Loop direct semantic control, Intent→Capability provider selection, Intent→World Truth. No verified duplicate Intent producer found.

## Walkthroughs

1. Normal: build Intent candidate and governed handoff; A uses it as context.
2. Invalid owner: ownership guard rejects a candidate; no mutation occurs.
3. Changed task/context: issue a new version/handoff; A evaluates cognitive impact; Loop only stores refs.

## Overlap, gaps, evolution, disposition

Overlap: `TERMINOLOGY_OVERLAP` with Goal/Concern/Task; possible `ADAPTER_GAP` to Working Envelope. No authority leakage proven. It may evolve into a governed Intent state/handoff service, never a Need/Capability/Loop owner. **Disposition: KEEP**.

**Ledger summary:** authority = Intent ownership/governed handoff; responsibility = Intent validity/provenance; state = governed candidate/current Intent refs; receiver = A/Causal governance; confidence = medium.
