# Conceptual Brain API Surface Design

This is a conceptual contract only. No API is implemented in this phase.

## Goal Governance API

- Input: Goal candidate, source/provenance, priority/conflict/policy refs.
- Output: Goal admission, priority, suspension, supersession, or termination decision/ref.
- Caller: governance entry or admitted upstream request.
- Authority: Brain.
- Responsibility: Brain.

## Concern Governance API

- Input: Concern candidate or existing Concern ref, Goal ref, source state, merge/split evidence.
- Output: ADMIT, REJECT, DEFER, MERGE_WITH_EXISTING, split/supersede governance decision.
- Caller: Brain or candidate-producing A/B modules through governance handoff.
- Authority: Brain.
- Responsibility: Brain.

## Grant Governance API

- Input: requested receiver, Work/Concern scope, authority set, safety/permission/resource envelope, state versions.
- Output: scoped grant, revocation, expiry, or rejection ref.
- Caller: Brain governance; A may request B derived scope.
- Authority: Brain, with bounded derivation rules.
- Responsibility: Brain for grant validity and global scope.

## Global Constraint API

- Input: safety, permission, resource, priority, and global availability evidence.
- Output: policy envelope, block, pause, revoke, or priority decision.
- Caller: governed modules and change propagation.
- Authority: Brain/global governance.
- Responsibility: Brain for global policy.

## Outcome Adjudication & Assimilation API

- Input: Outcome Evaluation candidate, A/B/Loop refs, Goal/Concern refs, current global policy.
- Output: accept/reject/defer/supersede/assimilate decision and handoff refs.
- Caller: Outcome Evaluation Governance, A, Loop, external completion boundary.
- Authority: Brain for global adjudication.
- Responsibility: Brain for global assimilation; source owners retain their own mutations.
