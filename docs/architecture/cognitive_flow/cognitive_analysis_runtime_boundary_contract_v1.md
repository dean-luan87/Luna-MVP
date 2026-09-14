# A3 Cognitive Analysis Runtime Boundary Contract v1

## Status and Authority

This is a planning boundary contract, not an executable Contract. It does not alter `cognitive_analysis_object_contract_v1.json` or authorize Runtime. `runtime_authorization_status: NOT_AUTHORIZED`.

## Future Input Boundary

| Input | Required boundary | Required validation | Forbidden substitution |
| --- | --- | --- | --- |
| Context Reference | `CurrentCognitiveContextV1` reference with version and trace linkage | reference present, lifecycle visible, provenance/trace usable | raw Field State, Snapshot mutation handle, database query |
| Evidence Reference | governed evidence identity with provenance and lifecycle signal | traceable; revoked/stale/unknown states retained | raw model output, observation capture, Fact claim |
| Hypothesis Reference | existing Hypothesis Candidate or competing-set reference | candidate identity, source Context/Frame linkage, lifecycle visible | Fact, forced dominant candidate, causal certainty |
| Analysis Question | declared scope/question with task/goal context where applicable | non-empty scope, trace and permission context available | Decision instruction or Action command |

## Future Output Boundary

| Output | Allowed meaning | Mandatory content | Never becomes |
| --- | --- | --- | --- |
| Analysis Result Candidate | candidate-only analysis result | source Context/version, result status, provenance, trace | Fact, Event, Field State, Decision |
| Evidence Trace | references showing used/supplied evidence lineage | evidence refs, relation/lifecycle signal, trace refs | evidence mutation or source replacement |
| Confidence / Uncertainty | explicit candidate assessment | uncertainty, coverage, contradictions, unresolved signals | Fact admission or truth score |
| Warning | explicit limitation or risk signal | stable warning/reason code and relevant ref | silent completion or authorization override |

## Mandatory Boundary Invariants

- A2 remains responsible for Context Construction; A3 reads Context by reference only.
- Field State Reducer remains the sole State mutation authority.
- Hypothesis Candidate is not Fact; confidence is not Fact authority.
- Unknown, stale, revoked, insufficient, conflicting, and blocked conditions remain explicit.
- Observation requests remain candidates and cannot execute through A3.
- A3 output may be read by a future Decision Candidate domain only through a separately governed handoff.

## Absolute Prohibitions

The future A3 Runtime must not:

- mutate Field State, Snapshot, Context, Event, Evidence, or a Fact Store;
- promote a Hypothesis, confidence value, or model output to Fact;
- invoke or execute Decision, Action, Observation, Reducer, or Admission behavior;
- use LLM, Vision Model, OCR, SLAM, database, network, camera, sensor, system time, randomness, or automatic UUID generation without a separately approved adapter and boundary revision.

## Boundary Failure Handling

Any attempted State mutation, Fact promotion, Decision/Action execution, Context/Snapshot writeback, ungoverned external capability use, or bypass of independent verification is a `blocker`. Missing, stale, revoked, unknown, or insufficient inputs must produce candidate warnings/blocks; they must not be silently repaired by Runtime.
