# Model Selection Decision v1

## Preliminary decision

| Candidate | Decision | Intended use | Reason |
| --- | --- | --- | --- |
| Expected Utility | Adopt as a bounded candidate | outcome/value/cost estimate | directly maps Belief, Value, Self cost; needs hard constraints |
| MCDA | Adopt as a comparison aid | multi-dimensional ranking and sensitivity | preserves conflicting criteria better than one fixed weight |
| Information Gain | Adopt for exploration candidates | value of reducing uncertainty | makes exploration decision-relevant and cost-aware |
| POMDP | Defer | future sequential simulation / B Route research | requires world/state/action transition assumptions |
| RL Reward Model | Reject as core | none | proxy reward can replace Luna's values and encourage manipulation |
| Pure unconstrained optimization | Reject as core | none | cannot safely represent unknowns, irreversibility, and hard boundaries |

## Adoption conditions

The three adopted candidates are not yet frozen as a formal Value Architecture.
Before adoption, synthetic cases must show:

1. a hard safety violation rejects a high-benefit candidate;
2. low battery or high cost changes ranking without changing the Goal;
3. unknowns remain explicit and reduce confidence rather than becoming facts;
4. MCDA sensitivity exposes unstable rankings;
5. Information Gain favors decision-relevant observations over curiosity;
6. current Reality and Self boundaries override stale Memory or optimistic
   probability candidates.

## Open questions

- Should Luna retain vector-valued candidates rather than immediately
  scalarize them?
- How should incomparable values be represented without fake precision?
- What calibration evidence is sufficient for a Probability Candidate?
- Which risks are hard constraints and which are tradeable context?
- How should user attention cost be bounded independently from compute cost?

Until these questions are answered, no numeric coefficients, automatic score,
or model package is canonical.
