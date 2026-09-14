# Task Lifecycle, Readiness and Completion v1

## Lifecycle

Conceptual vocabulary is:

`candidate/planned → ready → active/executing → waiting/paused → completed,
partially completed, failed, cancelled, or superseded`.

Existing `TaskState` and `TaskReadiness` enums contain candidate/hold/blocked/
paused/observation-review states. No enum changes are proposed.

## Readiness

Task readiness aggregates supplied refs for:

- required Decision;
- dependencies;
- permission/resource/safety;
- required environment conditions;
- executable capability candidate;
- required observation/evidence.

Task may aggregate readiness but cannot perform Runtime Admission or fabricate
source health. Capability, Brain/global governance, Observation, and source
owners provide the underlying evidence.

## Completion

Task owns completion-condition definition and contract-level completion
evaluation. Completion evidence comes from downstream execution or governed
refs. It does not declare Goal success, World Truth, A Sufficiency, or Intent
completion.
