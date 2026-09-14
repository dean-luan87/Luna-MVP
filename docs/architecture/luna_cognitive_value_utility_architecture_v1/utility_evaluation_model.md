# Utility Evaluation Model v1

Utility is a candidate estimate of expected gain relative to finite cost and
risk. It is not a prediction engine and it is not a decision.

```text
Expected Benefit × Importance × Probability
          − Resource Cost × Risk Factor
                         ↓
                  Utility Candidate
                         ↓
             Hard Constraint Check
                         ↓
              Priority Candidate
```

The phase reserves ROI as a supporting view:

```text
ROI = (Value Gain − Cost) / Cost
```

ROI cannot override a hard constraint. Inputs remain traceable to Field,
Goal, Belief, Capability, Experience, Self Resource, and Constitution context.
No computation, automatic scoring, ranking execution, or action selection is
implemented here.
