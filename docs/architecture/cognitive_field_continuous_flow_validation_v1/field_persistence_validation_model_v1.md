# Field Persistence Validation Model v1

## Persistence checks

For each time slice, the fixture compares:

- Stable Layer: Identity, Survival Constitution, Core Capability;
- Adaptive Layer: current Goal context, Attention scope, Field rules;
- Transient Layer: temporary task and event context;
- Field lifecycle and Transition Package;
- Unknown, Provenance, validity, and resource constraint.

## Expected behavior

Stable state persists across Home, Commute, Office, Commercial, and Home fields.
Adaptive state changes with context. Transient state is created, suspended,
closed, or released according to validity. Persistence does not turn a Field into
Memory or create Personality. Persistence is not Memory.

## Failure signals

State inflation, lost context, premature Unknown deletion, Identity Drift,
cross-field leakage, and unauthorized Decision output are validation failures.
