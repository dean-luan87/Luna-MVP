# RuntimeAdmissionAssessmentCandidateV1 Contract

## Purpose

This candidate records a governed assessment of whether a logically resolved
Capability has enough current evidence to become executable. It is an
assessment candidate, not execution and not a Provider call.

## Required evidence inputs

The candidate carries refs for:

- logical capability and slot;
- model asset and version;
- governed model path;
- declared checksum metadata;
- observed integrity evidence;
- dependency health;
- device/runtime health;
- Provider compatibility;
- permission, resource, safety;
- source/acquisition context and source state version;
- trace/provenance.

The candidate must preserve unknown or missing evidence. Missing evidence must
produce a blocked/deferred status, never an implicit approval.

## Output

The candidate returns:

- `admission_candidate_ref`;
- `admission_status` using existing status vocabulary where possible;
- `admitted_model_asset_ref` when admitted;
- `admitted_provider_compatibility_ref` when admitted;
- `blocking_reason_refs`;
- evidence refs;
- valid state version;
- expiry/staleness refs;
- trace/provenance refs.

## Admission authority

Capability Admission Governance is the decision authority for this combined
candidate. Model Manager, Diagnostics, Runtime Health, Provider Governance and
Observation/FPO remain evidence or subordinate qualification owners.

## Non-execution invariants

The candidate does not load a model, compute a checksum, probe dependencies,
probe runtime health, invoke a Provider, mutate memory/world state, or create a
cognitive Need.

