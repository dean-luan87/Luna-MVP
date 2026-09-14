# Scenario Replay Analysis

Source artifacts reviewed:

- `_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/cognitive_trace.json`
- `_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/cognitive_trace_summary.md`
- `capabilities/midplatform/sandbox/cognitive_exploration/cognitive_exploration_sandbox_fixture_v1.py`

## Scenario 12

The observed trace is:

| Round | Required conditions | Coverage / state change | Need | Branches | Strategies |
| --- | --- | --- | ---: | ---: | ---: |
| 0 | `signage`, `flow` | neither covered | 1 | 2 | 2 |
| 1 | `signage`, `flow` | `signage` added to coverage | 1 | 1 | 1 |

The Round 1 result is internally consistent with the current contracts:

1. The fixture creates one rule for each condition.
2. Each rule gets its own `minimum_set_ref`.
3. Each rule declares its own condition as its satisfaction coverage.
4. The engine therefore selects both as independent required conditions.
5. Adding `signage` coverage satisfies only the signage condition.
6. `flow` remains an unresolved condition, so Need, Branch, and Strategy remain
   for flow.

The trace does not show that Luna concluded “flow is required after signage was
insufficient.” It shows that the fixture encoded flow as an independent
requirement before the run began.

## Classification of the root cause

### A — Fixture modeling error

**Yes, as the immediate scenario-modeling error.** If the intended question is
only “what is the exit direction?”, then declaring `signage` and `flow` as two
independent required conditions over-specifies the objective. The fixture
should have represented one semantic requirement and separate possible basis
references.

### B — Canonical acquisition-oriented over-specification

**Partially, as an expressiveness limitation; not as a proven implementation
bug.** The current canonical contract legitimately treats each supplied
`condition_ref` as a governed condition. It does not know that `signage` and
`flow` were intended as source/path alternatives. The contract therefore
permits an upstream governance input to over-specify acquisition sources as
requirements.

### C — Missing minimum-sufficient / alternative-basis capability

**Yes, this is the primary architecture finding.** There is no explicit
canonical relation of the form:

```text
one Cognitive Requirement
→ one-or-more governed alternative Satisfaction Bases
```

Without that relation, a fixture correction alone cannot faithfully preserve
multiple acquisition paths while allowing one valid path to satisfy the shared
requirement.

## Other reviewed scenarios

| Scenario | Observed trace | Review interpretation |
| --- | --- | --- |
| 01 Single Clear Cue | 1 Need → 1 Branch → 1 Strategy | Consistent simple path; does not test alternatives. |
| 02 Unknown Exit | 1 Need → 3 Branches → 3 Strategies | Shows explicit multi-path basis projection, but the three condition refs are also modeled as separate requirements. |
| 03 Agree | 1 Need → 2 Branches → 2 Strategies | Agreement is retained as independent strategy lineage; no fusion. It does not prove alternative satisfaction. |
| 04 Conflict | 1 Need → 2 Branches → 2 Strategies | Conflict is preserved; no winner. It does not establish which source can satisfy the same requirement. |
| 07 Multiple Unknowns | 1 Need → 3 Branches → 3 Strategies | Demonstrates one branch per unresolved condition/gap under current model. |
| 10 No Strategy | 1 Need → 1 Branch → 0 Strategies | Honest governed absence; Need remains unresolved. |
| 11 Irrelevant Change | Round 0 and 1 remain 1/1/1 | Stability behavior is present for the sandbox seam. |
| 12 Evidence Update | Flow-only remainder survives after signage coverage | Correct under current conjunction semantics, insufficient for minimum-sufficient exit semantics. |

## Correct semantic model for the example

The review recommends this conceptual decomposition:

```text
Problem: find exit

Cognitive Requirement:
  exit_direction_known

Alternative Satisfaction Bases:
  reliable signage evidence
  trusted map/spatial evidence
  sufficiently valid human-flow/environment evidence

Acquisition Paths:
  inspect signage
  inspect flow
  inspect spatial structure
```

The last two layers remain separate. An acquisition strategy may propose how
to obtain a basis; it must not become a Required Condition merely because it is
one possible route.
