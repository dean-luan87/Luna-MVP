# Luna Causal Architecture Planning v1

Status: PLANNING_CANDIDATE

## Phase Position

This phase defines Luna first-version causal architecture planning artifacts only. It does not implement a runtime causal engine, model invocation, database write path, decision execution, action trigger, or task creation.

Causal layer responsibility: govern candidate-level explanations for why something may have happened, under evidence, uncertainty, conflict, temporal ordering, and provenance constraints.

## Canonical Owner

Canonical owner in this phase: Causal Governance.

Owner alignment note:
- Legacy planning assets may use Causal Reasoning Governance.
- This phase freezes Causal Governance as canonical owner for forward compatibility with Intent-to-Causal consumer naming.
- Legacy naming is treated as alias metadata only, not a second owner.

## Core Semantic Separation

Causal planning must separate:
- observation
- association
- correlation
- inference
- causal hypothesis
- causal support
- causal conflict
- causal uncertainty
- causal candidate/result
- decision

Hard guards:
- temporal precedence is not causality
- correlation is not causality
- model output is not causal fact
- memory prior is not causal fact
- intent preference is not causal conclusion
- emotional state is not causal authority
- field context is not causal authority
- causal hypothesis is not decision
- causal result is not action
- causal layer must not create task

## Candidate Flow

Source-owned influence references
-> Causal Hypothesis Candidate
-> Evidence Support/Opposition Update
-> Multi-Hypothesis Coexistence/Competition
-> Revision/Suspension/Revocation Candidate
-> Causal-to-Decision Handoff Candidate

## Boundary

Allowed inputs to Causal:
- evidence refs
- influence refs
- context refs
- prior refs
- intent refs

Forbidden:
- direct mutation of Intent/Field/Context/PCN/Memory/Emotion/Observation/Role
- direct decision output
- action instruction
- task creation

## Scenario Coverage

This phase defines 12 minimum planning scenarios to support direct fixture conversion in the next stage.

## Stop Condition

After planning assets and read-only verifier are created, stop at WAITING_FOR_USER_TERMINAL_VERIFICATION.
