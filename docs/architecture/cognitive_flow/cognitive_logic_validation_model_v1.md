# A-Route Cognitive Logic Validation Model v1

## Stage and boundary

Level 1 validates the cognitive logic that forms a Situation Candidate. It
tests this frozen slice only:

```text
Evidence → World Representation + Self Representation + Goal / Resource Context
                                      ↓
                              Situation Candidate
```

It does not test Decision, Action, Outcome, Experience, B Reflection, models,
VLM, OCR, SLAM, hardware, Runtime, or a Scheduler. All cases are deterministic
fixtures. A fixture assertion is a contract check, not a claim of intelligence
or real-world truth.

## Required cognitive rules

| Rule | Expected result | Forbidden shortcut |
|---|---|---|
| Self–World Coupling | identical World State can yield different Situation Candidates when Self changes | universal answer based only on world facts |
| Capability Boundary | limited sensing yields evidence-insufficient or adaptation-needed context | capability-to-false-confidence conversion |
| Unknown Preservation | ambiguous observation remains Unknown | unsupported object/reality assertion |
| Reality Grounding | facts, hypotheses, and risk/observation candidates stay separated | hypothesis presented as fact |
| Situation Re-evaluation | material new Evidence forms a revised Situation Candidate | retain stale situation after environmental change |

## Structured cognitive trace

Each deterministic case uses this non-CoT output contract:

```json
{
  "world_state": {},
  "self_state": {},
  "goal_context": {},
  "resource_context": {},
  "situation_candidate": {},
  "confidence": {},
  "unknowns": {},
  "reasoning_trace": {
    "evidence_refs": [],
    "self_capability_refs": [],
    "relevant_constraints": [],
    "situation_update_reason": "candidate"
  }
}
```

The reasoning trace is structured provenance and relation metadata. It must not
contain private chain-of-thought, a Decision, an Action, or a truth claim.

## Logic validation metrics

The five Level 1 metrics are Self Awareness, Reality Grounding, Unknown
Management, Situation Adaptability, and Confidence Calibration. They check
whether a trace has the required cognitive boundaries; they do not score answer
accuracy, optimize a task, or modify an A-route state.
