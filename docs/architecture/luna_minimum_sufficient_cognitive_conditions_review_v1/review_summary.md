# Cognitive Logic Review: Minimum Sufficient Cognitive Conditions v1

Phase: `Phase-Cognitive-Logic-Review-Minimum-Sufficient-Cognitive-Conditions-v1-001`

Status: `COGNITIVE_SUFFICIENCY_REVIEW_COMPLETE`

## Review decision

Scenario 12 exposes a real modeling limitation, not a failure of the Sandbox
runtime. The immediate fixture declares `signage` and `flow` as two separate
required conditions. The deeper architecture currently has no explicit
separation between one cognitive requirement and its alternative satisfaction
bases.

The finding is therefore:

```text
PRIMARY FINDING = C — current architecture lacks explicit
                   minimum-sufficient / alternative-satisfaction expression
MANIFESTATION    = the Scenario 12 fixture over-specifies acquisition sources
```

This is not a reason to reopen the closed Information Need, Branch, or Strategy
phases. It is a sufficiency-semantics review before Strategy Coordination.

## Current canonical chain

```text
Governed Objective Condition Rules
→ Required Cognitive Condition Formation
→ Current Cognitive Coverage subtraction
→ Information Need Candidate
→ unresolved Information Gap
→ Cognitive Branch Candidate
→ Branch Governance
→ explicit Acquisition Strategy Candidate
```

The current chain treats each independently applicable `condition_ref` as a
required cognitive condition. It can preserve a satisfied condition as
required, but it does not yet represent that several alternative evidence
bases may satisfy one shared cognitive requirement.

## Required distinction

```text
Cognitive Requirement
  = what must be known for the objective

Satisfaction Basis
  = an evidence/coverage form that can satisfy that requirement

Acquisition Path
  = a candidate way to obtain a satisfaction basis
```

For `find exit`, the semantically minimal requirement is approximately
`exit_direction_known`. Signage, map/spatial evidence, and sufficiently valid
flow/environment evidence are possible satisfaction bases. Inspecting those
sources are acquisition paths. They should not automatically become three
conjunctive Required Cognitive Conditions.

## Recommendation

Recommend **Option B — Semantic Cognitive Requirement + Alternative
Satisfaction Basis** as the next architecture direction, after a targeted
fixture correction and a separately approved implementation.

Option C is not needed yet: multiple sufficient condition sets would add
larger set/Boolean semantics before the simpler requirement/basis distinction
has been established.

## Strategy Coordination decision

`BLOCKED_BY_COGNITIVE_SUFFICIENCY_SEMANTICS`

Strategy Coordination should not be started while the system can interpret
multiple acquisition sources as jointly required when one source can already
satisfy the objective. Otherwise coordination may optimize or schedule an
incorrect requirement set.

## Scope decisions

- Fixture correction: **YES**, for the Scenario 12 semantic intent; not applied
  in this review.
- Schema change: **YES**, if Option B is adopted; only a thin governed
  requirement-to-basis expression is needed, not a new framework.
- Canonical runtime code change: **YES**, later, to evaluate alternative basis
  satisfaction; not applied in this review.
- Ownership change: **NO**. Required-condition and Need sufficiency remain on
  the A-Route cognitive side; Strategy Coordination does not become the owner.

No runtime, Contract implementation, Sandbox, or existing phase document was
modified by this review.
