# First Controlled Migration Cut Line

## Recommendation

The smallest coherent first migration is candidate-only and adapter-level:

1. introduce a new reference-only CognitiveWorkingEnvelope design;
2. introduce A-to-Loop mechanical command candidates;
3. introduce Loop-to-A mechanical state return candidates;
4. wrap existing Dynamic Flow decisions behind an A-owned adapter;
5. preserve existing Dynamic Flow and Loop engines internally;
6. do not rewire real Provider, B1/B2/B3/B4 or runtime paths yet.

## Likely source files

New same-owner integration files would likely live under:

capabilities/midplatform/core/cognitive_flow/integration/

Likely future adapter locations:

- existing Dynamic Cognitive Flow integration package;
- existing cognitive_loop_governed_continuity_candidate_controlled package;
- existing A Route orchestration integration package.

The exact files should be confirmed during the implementation inventory. No
file is changed by this contract phase.

## Required adapter behavior

The future A-owned adapter may:

- construct a Working Envelope from existing read-only refs;
- translate A semantic candidate decisions into mechanical Loop commands;
- pass commands to existing Loop mechanics;
- translate Loop mechanical returns back into A-readable state facts;
- preserve source state version, trace and provenance.

It must not:

- change canonical enums;
- make Loop infer semantic decisions;
- make Task control Loop cognition;
- create B independently;
- invoke Provider/model runtime;
- delete verified engine behavior.

## Stop condition

Stop the first migration when the candidate path proves:

Brain-governed concern
→ A semantic decision
→ mechanical Loop command
→ mechanical Loop state return
→ A reassessment

No B runtime, real capability invocation, Semantic Module, Filter runtime,
Experience mutation or Action execution should be included in this cut line.
