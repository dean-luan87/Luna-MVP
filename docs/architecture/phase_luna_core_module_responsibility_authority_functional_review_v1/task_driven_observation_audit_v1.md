# Task-Driven Observation Audit v1

Task-driven observation assets define request types, target module candidates,
freshness, priority hints, task refs and gates. They explicitly preserve
candidate-only, blocked-now, no-camera/no-OCR execution behavior.

Canonical separation:

1. Task declares an execution dependency or completion condition.
2. A decides whether the missing information is a Cognitive Need.
3. Attention produces a priority/budget candidate.
4. Observation/FPO admits and executes acquisition.
5. Evidence returns to A and/or Task completion evaluation through governed
   refs.

Historical Task paths that directly schedule observation or choose OCR/vision
must be narrowed to request/dependency candidates. They are not evidence that
Task owns Attention, Observation, or Provider selection.
