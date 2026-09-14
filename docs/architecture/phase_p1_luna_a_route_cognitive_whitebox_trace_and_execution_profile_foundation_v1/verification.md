# Verification Contract

## Runner

The synthetic Runner only builds trace/profile artifacts and writes a review
summary. It does not invoke providers, models, observation, action, or dataset
loading.

## Verifier

The structural Verifier checks:

- node owner/source and candidate boundaries;
- node order, parent and transition coherence;
- observation-cycle coherence;
- Hypothesis revision linkage;
- Sufficiency transition history;
- Information Gap and Re-observation linkage;
- Decision Governance handoff without Decision creation;
- explicit unavailable/planned semantics;
- gap attachment to trace nodes;
- TestBoard non-authority;
- all execution/mutation negative guards.

The Agent did not run either command. User-terminal commands:

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.runner_v1
python3 -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.verifier_v1
```
