# A3 Cognitive Analysis Result Consumer Governance Contract v1

## Position

This contract governs how future Cognitive Flow layers may **read** an `Analysis Result Candidate`. It is not a permission grant, handoff execution, Runtime authorization, Fact admission, Decision contract, or State authority.

All consumers must retain the result's evidence references, uncertainty, provenance, warning, and candidate-only status. `runtime_authorized=false` remains unchanged.

## Consumer Types

| Consumer Type | allowed_access | forbidden_access | required_evidence | required_trace |
| --- | --- | --- | --- | --- |
| Observation Layer | read result as an attention/observation candidate; read Evidence, Uncertainty, Provenance | Fact, Decision, Action, State, Memory operations | all supplied Evidence references | result trace and provenance retained |
| Context Layer | read result as a contextual signal; read Evidence, Uncertainty, Provenance | Context/Snapshot writeback, Fact, Decision, Action, State, Memory operations | all supplied Evidence references | result trace and provenance retained |
| Hypothesis Layer | read result as candidate support, contradiction, or uncertainty input; read Evidence and Provenance | forced hypothesis, Fact, Decision, Action, State, Memory operations | all supplied Evidence references | result trace and provenance retained |
| Decision Support Layer | read result as a bounded support signal; read Evidence, Uncertainty, Provenance | direct Decision creation, Action execution, Fact, State, Memory operations | all supplied Evidence references | result trace and provenance retained |
| Learning Candidate Layer | read result as a learning-input candidate; read Evidence, Uncertainty, Provenance | Experience/Memory update, Fact, Decision, Action, State operations | all supplied Evidence references | result trace and provenance retained |

## Permission Boundary

Every consumer declaration must include all four permitted read forms: `analysis_result_candidate`, `evidence_reference`, `uncertainty`, and `provenance`. It must explicitly deny Fact creation/mutation, Decision creation, Action execution, State mutation, and Memory update.

## Traceability Boundary

Consumers may not strip, replace, silently complete, or convert evidence/provenance/uncertainty. Missing, stale, revoked, conflicting, or unknown conditions remain visible to the consumer and must be handed forward as candidate limitations.

## L1 Alignment

This read-only boundary aligns with L1 Input/Output Candidate Governance, Input/Output Symmetry, Protocol Traceability, Permission/Admission, and Model/Skill Admission. It creates no parallel permission or admission system.
