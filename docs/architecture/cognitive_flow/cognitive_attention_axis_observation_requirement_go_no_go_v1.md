# Attention Axis and Observation Requirement Go/No-Go v1

## V0 static acceptance criteria

1. Attention Intent provides purpose, direction, context, time, confidence,
   priority, and trace candidates from an existing Brain need.
2. Attention Requirement expresses information need, evidence type, scope,
   region/object candidates, and unknowns without specifying a model.
3. Refinement converts Intent plus Situation/Capability/Experience references
   into Capability Observation Candidate without direct Provider selection.
4. Attention Axis covers direction, region, entity, attribute, and relationship
   without asserting existence or controlling a device.
5. Attention Feedback contains coverage, evidence, missing information,
   confidence, resource cost, and classified failure candidates.
6. Brain, Attention, Capability, Evidence, Reality Cognition, and Neural
   Regulation boundaries are distinct.
7. Attention Requirement != Automatic Frequency Adjustment.
8. Working Attention Context and Attention Pattern Candidate are governed;
   attention history is not written as Memory.
9. Multi-object, goal-change, resource-limit, failure, and Self-difference
   scenarios are specified.
10. No automatic model call, visual control, frequency adjustment, Scheduler,
    Attention Runtime, online learning, B Reflection, Action, or State mutation
    is introduced.

## Verification ownership

Execution Mode: `Planning Only`.

- V0 static artifact, contract, and verifier-syntax checks: Agent.
- V1 execution: not permitted.
- V2 final phase verification: user terminal only.
- V3 audit: ChatGPT only.

## User-terminal verification command

```bash
python3 docs/architecture/cognitive_reality_cognition_attention_axis_observation_requirement_v1/verify_cognitive_reality_cognition_attention_axis_observation_requirement_v1.py
```

`final_candidate_decision: COGNITIVE_REALITY_COGNITION_ATTENTION_AXIS_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
