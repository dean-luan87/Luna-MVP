# Ownership Decision

## Requirement and satisfaction ownership

Required Cognitive Condition Formation remains owned by:

`A-Route Cognitive Responsibility`

That boundary should own the governed interpretation of:

```text
objective applicability
→ currently relevant cognitive requirement
→ satisfaction by explicit current cognitive coverage/basis
```

Information Need Formation remains responsible for:

```text
required cognitive requirement
− satisfied/current cognitive coverage
→ necessary unknown
→ Information Need Candidate
```

It must not be moved to Strategy Coordination.

## Need satisfied / closed / reopened

A Need should become satisfied/closed for the current cognitive cycle when all
currently applicable cognitive requirements have at least one governed,
valid, sufficiently current satisfaction basis. A merely available acquisition
path is not satisfaction. A source label alone is not satisfaction.

If the accepted satisfaction basis becomes invalid, stale, contradicted, or no
longer applicable, the cognitive state must be able to form a new Need or
reopen the prior Need through the existing Need-side lifecycle semantics. This
decision belongs to the A-Route requirement/coverage/Need side, not Strategy
Coordination.

The existing implementation currently represents this as a fresh candidate
calculation: non-empty `necessary_unknown_refs` forms a Need, and an empty set
returns `NO_ACTIVE_NEED`. It does not yet provide explicit Need reopen
lifecycle semantics; that is a future concern, not implemented here.

## Overall Sufficiency and Stop

There are two related but distinct decisions:

1. **Requirement satisfaction:** whether each current cognitive requirement has
   a valid satisfaction basis. This belongs with Required Condition formation
   and Current Cognitive Coverage, feeding Information Need Formation.
2. **Loop continuation / stop:** whether the broader cognitive objective may
   stop or continue after considering the current cognitive state. This remains
   with the existing Sufficiency / Stop owner.

Strategy Coordination must consume the resulting semantic state; it must not
decide whether a source was enough for the objective.

## No owner changes

- Goal / Intent / Concern governance: unchanged.
- Required Cognitive Condition Formation: unchanged owner.
- Information Need Formation: unchanged owner.
- Branch Formation / Governance: unchanged owners.
- Acquisition Strategy Candidate Formation: unchanged owner.
- Sufficiency / Stop: unchanged owner.
- Strategy Coordination: not yet an owner for semantic sufficiency.

No Field, Current World, Self, Memory, PCN, Decision, Task, Action, Provider,
or Model authority is introduced.
