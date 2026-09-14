# Loop semantic retirement plan

## First cut

Add an adapter-level contract in which A/Brain supplies:

- current disposition;
- continuity impact;
- resume decision;
- stale Requirement disposition;
- closure reason and acceptance;
- growth decision.

Loop then records state, refs, pause/wait, freeze and history only.

## Safety rule

Do not delete `LoopLocalStateCandidateV1` fields while old fixtures still inspect them. First change producers to accept supplied semantic refs, then migrate fixtures/verifiers, then remove inference helpers.

## Cutover gate

The cut is complete only when no Loop engine function constructs semantic values from lifecycle or fixture inputs and the mechanical command verifier proves forbidden semantic commands are rejected.

