# Decision Architecture Plan v1

## Phase

- Phase: Phase-Luna-Decision-Architecture-Planning-v1-001
- Stage: Decision Architecture Planning
- Execution Mode: Planning Only
- Canonical owner: Decision Governance

## Planning Objective

Establish a first-version Decision Architecture Planning package that defines owner boundary, concept boundary, schema candidates, state semantics, constraint layering, handoff boundary, negative guards, and verifier contracts without implementing real decision runtime.

## In Scope

- Planning and contract candidates only.
- Candidate-only decision formation semantics.
- Decision to Action/Task handoff boundary contract.
- Minimum scenario suite for future executable fixtures.
- Read-only final phase verifier.

## Out of Scope

- Runtime decision execution.
- Any action execution, actuator command, or task creation.
- Any model/provider/device invocation.
- Any database, memory, or source mutation outside phase-local planning assets.

## Canonical Owner

Decision Governance is frozen as the sole canonical owner for this phase.
Legacy names are retained only as historical references and cannot create parallel mutation authority.

## Core Boundary Positioning

- Intent influences decision, but Intent is not Decision.
- Causal candidates influence decision, but Causal is not Decision.
- Selected decision candidate is not runtime execution.
- Decision is not Action and is not Task.
- Decision Governance consumes Permission/Safety/Role constraints but does not own or modify those policies.

## Planning Outputs

This phase produces planning-only files for:

- Owner and concept boundaries.
- Decision Candidate schema and state model.
- Option and multi-candidate coexistence model.
- Risk/Utility/Constraint separation model.
- Permission/Safety and influence boundaries.
- Defer/Abstain/Request-More-Evidence model.
- Reversibility and human confirmation boundaries.
- Resource degradation model.
- Provenance and revision lifecycle.
- Decision to Action/Task candidate-only handoff.
- Negative guards, reuse mapping, open questions, and verifier.

## Stop Condition

After all required planning artifacts are created and static checks are ready, stop at WAITING_FOR_USER_TERMINAL_VERIFICATION.
