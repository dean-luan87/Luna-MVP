# A-Route Cognitive Logic Validation Go / No-Go v1

## Acceptance contract

- Self–World Coupling fixtures retain one World State and vary Self State.
- Capability Boundary fixtures reject capability-to-false-confidence.
- Unknown Handling fixtures preserve ambiguity as Unknown.
- Reality Grounding fixtures separate fact, hypothesis candidate, and risk/observation candidate.
- Situation Reassessment fixtures supersede stale Situation Candidates after material evidence change.
- Each case uses the structured trace contract and excludes private chain-of-thought.
- Fixtures have no Decision, Action, Outcome, Experience, B Reflection, Runtime, model, Provider, or hardware path.
- Level 1 tests cognitive logic boundaries, not answer accuracy or task completion.

## Terminal verification

The user alone runs:

```bash
python3 docs/architecture/cognitive_reality_cognition_a_route_logic_validation_v1/verify_cognitive_reality_cognition_a_route_logic_validation_v1.py
```

Expected terminal state: WAITING_FOR_USER_TERMINAL_VERIFICATION.
