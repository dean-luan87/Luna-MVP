# Consolidated Regression — Future Contract

## Current consequence

The consolidated real-approved checkpoint currently forwards terminal-owned
readiness arguments to the existing Real Capability trial. This is appropriate
for the controlled trial, but it makes the checkpoint a transport owner of
values that should eventually be supplied by existing governance/evidence
owners.

## Future contract

```text
Checkpoint
  → requests approved Real Capability trial
  → trial obtains/adopts Model, Diagnostics, Integrity and Admission state
  → unchanged Provider admission
  → Provider invocation only if admitted
```

The checkpoint must not approve dependencies, calculate or invent checksums,
choose model/provider identity, or silently replace unresolved defaults.

## Regression invariants to preserve

- maximum Provider invocation remains one;
- `REQUEST_MORE_EVIDENCE` does not create an automatic second invocation;
- blocked admission means no Provider invocation;
- A/Dynamic Flow/Loop semantic boundaries remain unchanged;
- failure reports distinguish readiness evidence from Provider failure;
- terminal arguments remain explicit until a governed source exists.

