# ExecutableCapabilityCandidateV1 Contract

## Meaning

`ExecutableCapabilityCandidateV1` means that the logical Capability has passed
the separate Runtime Admission assessment for the referenced state/version.
It is still a candidate handoff. It does not execute anything.

## Required proof

The candidate must reference:

- the Runtime Admission candidate;
- logical capability and slot;
- admitted model asset and model version;
- governed path ref;
- admitted Provider compatibility ref;
- valid source/state version;
- permission/resource/safety refs;
- expiry/staleness refs;
- trace/provenance.

## Provider boundary

The candidate may be consumed by the existing Provider Admission contract. It
does not authorize autonomous Provider execution. Provider admission remains a
separate boundary and must preserve the existing bounded request and evidence
requirements.

## Invalid construction

No executable candidate may be produced when the Runtime Admission status is
blocked, unresolved, expired, stale, permission-denied, resource-denied, or
missing required integrity/dependency/runtime evidence.

