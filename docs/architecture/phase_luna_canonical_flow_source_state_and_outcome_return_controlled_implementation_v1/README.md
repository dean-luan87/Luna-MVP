# Controlled Source-State and Outcome Return Implementation v1

## Scope

This implementation slice creates only candidate-only seams for:

- Evidence/Provider/Action Result → Source-State Handoff Candidate;
- Current World and Field Event independent candidate adapters;
- Outcome Candidate → Brain Adjudication Input Candidate;
- canonical edge observability;
- synthetic fixture, Runner and Verifier assets.

## Hard guarantees

No source mutation, Field Reducer execution, Current World authoritative write, Brain execution, Brain state mutation, Intent/Task/Memory/Experience mutation, Learning, Provider invocation, Action execution, or runtime execution is permitted by the local guards.

## Verification ownership

The Runner and Verifier are intentionally not executed by the agent. User terminal verification is required.

