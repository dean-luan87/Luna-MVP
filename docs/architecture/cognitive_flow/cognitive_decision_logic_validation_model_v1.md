# A-Route Decision Logic Validation Model v1

## Stage and scope

Level 2 validates the logic from a formed Situation Candidate through Option
Generation and Decision Evaluation to a Decision Candidate:

```text
Situation Candidate
      ↓
Option Generation Candidate Set
      ↓
Decision Evaluation Candidates
      ↓
Decision Candidate
      ↓
Brain Evaluation Candidate
```

This phase excludes Action Execution, hardware, Provider, Runtime, Outcome,
Experience Adoption, B Reflection, and the Emotional Engine. All fixtures are
deterministic contract inputs. They test cognitive trace boundaries rather than
task success, policy optimization, or real-world answer accuracy.

## Frozen rules

| Rule | Required condition | Prohibited condition |
|---|---|---|
| Decision ≠ Action | Decision Candidate identifies a selected option only | motion command or execution implementation |
| Situation dependency | option/evaluation trace refers to Situation, Self, Goal, Resource, and risk | direct choice from a single Evidence item |
| Constraint-bounded reasonableness | choice is evaluated under current constraints | theoretical absolute-optimal assertion |
| Unknown visibility | confidence and evaluation retain Unknowns | hidden uncertainty or fabricated certainty |
| Reconsideration | material new Evidence may form a new option/evaluation set | immutable prior Decision Candidate |
| Brain authority | Brain Evaluation remains final cognitive judgment boundary | Neural, Provider, Experience, or fixture selecting the decision |

## Required evaluation dimensions

Every option evaluation records: Survival Impact, Goal Alignment, Capability
Fit, Resource Cost, Risk, Uncertainty, Experience Reference, and Confidence.
An absent Experience Reference remains explicit; it never blocks a valid
candidate or becomes a direct strategy override.

## Level 2 output

Fixtures use a structured decision trace, not private chain-of-thought. The
trace may describe evidence links, constraints, option attributes, unknowns,
and candidate rationale categories. It must not expose private reasoning,
create an Action, claim Outcome, or mutate State.
