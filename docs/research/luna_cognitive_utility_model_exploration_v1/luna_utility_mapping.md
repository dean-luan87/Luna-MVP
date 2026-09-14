# Luna Utility Mapping v1

| Mathematical concept | Luna source | Luna responsibility | Candidate output | Boundary |
| --- | --- | --- | --- | --- |
| Probability | Belief, Capability, Experience | expose calibrated/uncertain estimate | Probability Candidate | never treated as fact |
| Outcome Value | Value Hierarchy, Goal, Field | contextualize what would matter | Benefit Candidate | does not create Goal |
| Cost | Self Resource, Self Rhythm, Capability State | expose finite resource impact | Cost Candidate | does not control Runtime |
| Risk | Self Regulation, Constitution, Field, Unknowns | identify hard and soft risk | Risk Candidate | hard safety can reject |
| Expected Utility | probability + value − cost | combine outcome candidates | Utility Candidate | no automatic score |
| MCDA | Value dimensions + criteria | preserve multiple criteria | Priority/Tradeoff Candidate | no scalar authority |
| Information Gain | Uncertainty + decision impact | estimate value of observation | Exploration Utility Candidate | bounded exploration only |
| POMDP | future B Route state/belief models | simulate sequential uncertainty later | Simulation Candidate | not current Value |

## Pipeline mapping

```text
Understanding
    ↓
Goal Candidate
    ↓
Candidate alternatives / exploration candidates
    ↓
Belief + Value + Self Resource + Risk context
    ↓
EU / MCDA / Information Gain candidate calculations
    ↓
Hard Constraint Check
    ↓
Priority / Tradeoff Candidate
    ↓
Brain and future Decision Arbitration review
```

The pipeline produces decision support, not a Decision. It does not write
Reality, mutate Goal, update Value, execute Action, or learn from an outcome.

## Model ownership

- Constitution owns hard constraints.
- Self owns resource and stability context.
- Value Layer owns value interpretation and candidate evaluation contracts.
- Goal Layer owns direction and goal governance.
- Exploration Governance owns exploration admission candidates.
- Brain owns cognitive judgment.
- Future Decision Arbitration may compare admitted candidates; it is not
  implemented here.

External libraries, if later admitted, are numerical helpers behind an adapter.
They must not receive direct access to Self, Memory, Goal, Reality, or Action
state.
