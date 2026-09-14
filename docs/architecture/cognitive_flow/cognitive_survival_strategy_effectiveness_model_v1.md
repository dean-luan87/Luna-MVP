# Survival Strategy Effectiveness Model v1

## Evaluation unit

This model evaluates a recurring **strategy pattern**, not a single Action or
single event. A single outcome may be informative, but cannot establish that a
strategy is effective or ineffective.

```text
Strategy Pattern + Situation Class + Outcome References + Value Feedback
                                   ↓
                 Strategy Effectiveness Candidate
```

## Assessment fields

| Field | Meaning |
|---|---|
| `strategy_scope` | situation class and stated survival contribution |
| `observed_effect_pattern` | repeated outcome/value pattern with traceability |
| `benefit_candidate` | candidate physical, capability, relationship, or meaning contribution |
| `cost_or_friction_candidate` | candidate resource cost, uncertainty, or relationship friction |
| `confidence_and_unknowns` | support level and unresolved confounders |
| `adjustment_candidate` | candidate to refine observation, capability usage, or communication strategy |

Example: “proactively remind about maintenance” may be beneficial when it
results in accepted maintenance and stable cooperation. High-frequency
reminders may instead reveal long-term relationship friction. Neither single
case directly changes strategy.
