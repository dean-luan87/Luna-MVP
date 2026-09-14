# Verification Contract

## User-terminal execution

The controlled runner and verifier are supplied under
`capabilities/evaluation/a_route_required_cognitive_condition_formation/`.
The Agent does not run Python, the runner, verifier, Provider, Model, or
Observation Runtime.

The runner marker is:
`CONTROLLED_A_ROUTE_REQUIRED_COGNITIVE_CONDITION_FORMATION_TEST`。

## Required behavior

The verifier covers:

- same Goal with a different current cognitive situation;
- relevant coverage change marking a required condition satisfied without
  removing it from the required set;
- different governed Role changing the active requirement;
- relevant Self state changing the active requirement;
- different Goal in the same situation;
- irrelevant information remaining stable;
- minimum-set selection retaining alternatives as dormant;
- compatibility with existing Minimum Relevant Cognitive View and Information
  Need formation APIs。

The controlled rule set is reused across cases. Case IDs are reporting labels,
not semantic inputs. Formation uses no scenario/case branch, goal keyword
matching, static Goal-to-Condition lookup, or opaque Context guessing.

The satisfaction compatibility rule is also covered: a rule with explicit
`alternative_satisfaction_basis_refs` is satisfied by any one currently
covered basis, while a rule without alternatives preserves exact legacy
coverage. A satisfied requirement remains in the active required set; only its
separate satisfaction result is used by downstream Need subtraction.

## Required guards

All results remain `candidate_only=true`, `read_only=true`,
`truth_declared=false`, and `world_truth_declared=false`. Goal, Intent, Concern,
Role, Context, Field, Self, Current World, Memory and PCN mutation are false。

Provider/Model invocation, Observation execution, Observation Demand formation,
Capability selection, Decision, Task and Action are false. The formation engine
does not re-enter Information Need Formation and does not consume an existing
Need, so the dependency remains one-way:

```text
Required Conditions → Minimum View / Current Coverage → Information Need
```

## Maturity claim

Even if all user-terminal checks pass, the claim is limited to
`Governed State-Sensitive Required Cognitive Condition Formation`。It is not a
claim of Autonomous Goal Understanding, generalized semantic cognition,
generalized planning, or commonsense reasoning。
