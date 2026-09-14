# Intent Runtime Gap v1

## Existing assets

The repository contains a controlled Intent Governance package with core
candidate types, lifecycle and interaction candidate types, a skeleton
assembler, static validators, ownership guards, trace candidates and a
candidate handoff. The input/output envelope is synthetic/candidate-only and
does not mutate source state.

## Gap classification

| Gap | Classification | Impact |
|---|---|---|
| unified admitted Intent record/API | RUNTIME_GAP | lifecycle authority is not yet operational |
| candidate → admission bridge | ADAPTER_GAP | no single production handoff to Working Envelope/A |
| multi-Intent persistent active set | RUNTIME_GAP | interactions are candidate-only |
| Brain global-priority integration | CONTRACT_GAP / ADAPTER_GAP | policy inputs exist conceptually, bridge is incomplete |
| source-version invalidation propagation | ADAPTER_GAP | source refs exist, downstream invalidation is not unified |
| terminology around active vs active-candidate | TERMINOLOGY_GAP | older prose can overstate authority |
| independent Intent owner | NO_GAP | registry and contracts identify `Intent Governance` |

These are not reasons to move ownership to Brain, A or Task. The next phase
should specify an admission/lifecycle contract; it must not invent a new
Manager or change canonical owners.
