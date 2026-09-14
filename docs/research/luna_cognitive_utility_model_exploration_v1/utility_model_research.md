# Cognitive Utility Model Exploration v1

## Purpose and boundary

This research note tests whether Expected Utility, MCDA, Information Gain,
and POMDP concepts are suitable foundations for Luna's future Value Layer. It
does not freeze a Value Architecture, install a library, run a model, or
create a Runtime.

The working question is not “which action maximizes one scalar?” It is “which
candidate is worth evaluating under Luna's current Field, Goal, uncertainty,
finite resources, and hard safety boundaries?”

## Candidate model assessment

### Expected Utility Theory

Expected Utility is a useful candidate for an outcome-level estimate:

```text
Expected Utility = Probability × Outcome Value − Cost
```

Belief and Experience can provide a probability candidate, Value can provide
contextual outcome importance, and Self can provide cost and capability
constraints. The model is not sufficient alone: probabilities may be poorly
calibrated, scalar utility can hide conflicting dimensions, and a safety
violation must reject a candidate rather than become a small negative score.

**Assessment:** suitable as a bounded candidate calculation, subject to
unknown preservation, hard constraints, provenance, and Brain review.

### MCDA

MCDA is suitable for keeping several dimensions visible when alternatives have
different safety, mission, growth, information, resource, and risk profiles.
It can support a priority candidate and sensitivity analysis. Normalization,
weight elicitation, and aggregation must remain explicit; a single aggregate
score must not erase non-compensatory safety constraints.

**Assessment:** suitable as a comparison and ranking aid, not as authority for
Goal creation, Decision commitment, or Action.

### Information Gain

Information Gain is suitable for asking whether an observation or query is
worth the cost of reducing uncertainty. The Luna form is a candidate:

```text
Exploration Utility = Expected Information Gain − Exploration Cost
```

Information gain must be tied to a current Goal, Field, risk, and decision
impact. High curiosity with no decision relevance is not enough. Exploration
also requires Self resource approval and explicit stop conditions.

**Assessment:** suitable for exploration governance as a bounded value input;
not a license for open-ended search or automatic learning.

### POMDP

POMDP is a possible future representation for partially observed sequential
decision problems. It requires explicit state, action, observation, transition,
reward, belief, and horizon assumptions. Those assumptions belong to later B
Route / simulation or a controlled planning study, not to the current Value
Layer. POMDP therefore remains a future research interface, not a current
calculation core.

**Assessment:** defer. Do not introduce a POMDP runtime or world model in this
phase.

## Explicitly rejected foundations

An RL Reward Model is not adopted as Luna's core value definition. A reward
signal can turn user satisfaction or proxy metrics into a goal-substitution
pressure and can encourage proxy maximization instead of safe assistance.

A pure unconstrained optimizer is also rejected. A life-like subject needs
unknown preservation, non-compensatory safety, reversibility checks, and
resource governance that cannot be reduced to a scalar penalty.

## Preliminary conclusion

The most compatible stack is:

```text
Expected Utility candidate
        + MCDA dimension comparison
        + Information Gain for exploration
        + Constitution / Self hard constraints
        ↓
Priority Candidate → Brain / future Decision Arbitration
```

This is a research conclusion, not a frozen architecture. The next formal
Value Architecture should be admitted only after synthetic cases test
calibration, sensitivity, hard-constraint rejection, unknown preservation,
and resource degradation.

## Reference material

- [pyDecision package](https://pypi.org/project/pydecision/) — broad Python MCDA methods.
- [scikit-criteria documentation](https://scikit-criteria.quatrope.org/) — MCDA methods integrated with the scientific Python stack.
- [pomdp_py documentation](https://h2r.github.io/pomdp-py/) — general-purpose POMDP/MDP research interfaces.
- [Multi-Criteria Decision Analysis overview](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118644898) — MCDA and multi-attribute utility foundations.
