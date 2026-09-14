# Attention Existence Test v1

| Architecture | Assessment |
|---|---|
| Attention embedded in A | Fails separation: A Need and resource allocation become one authority. |
| Attention embedded in Brain | Fails locality/reuse: Brain would absorb modality, region and acquisition focus mechanics. |
| Attention embedded in Observation | Fails policy separation: executor would choose semantic focus and budget. |
| Attention embedded in Task | Fails reuse across non-task/safety/modality sources and risks a scheduler. |
| Independent narrow Attention Governance | **Preferred.** Separates Need from bounded focus allocation and is reusable across modalities. |
| Pure derived candidate without owner | Fails responsibility: no owner for competition, stale focus, budget and handoff validity. |

## Decision

Attention deserves an independent canonical boundary, but not an Attention
Manager or runtime component in this phase. The irreducible responsibility is
policy-constrained focus/priority/budget candidate allocation after A Need and
Brain constraints are available.

## Testability and replaceability

The boundary is observable through candidate refs, scores, source versions,
budget decisions, alternatives, conflict markers and provenance. A future
implementation can use heuristics, policy tables or learned ranking without
changing A, Brain or Observation ownership.
