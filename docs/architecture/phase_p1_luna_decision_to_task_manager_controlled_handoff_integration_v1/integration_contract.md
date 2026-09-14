# Integration Contract

A Task handoff is admitted only when the existing Decision Governance output
contains one selected candidate with `execution_eligibility_candidate=true`
and the candidate is eligible. The Decision output must remain candidate-only
and must not be an executed Decision.

The adapter maps the selected Decision ref, Decision trace ref, source
Decision handoff ref, context, constraints, permissions, safety, resources,
and provenance into the existing Task Manager request mapping. The Task
Manager output is a controlled Task state, not Task runtime execution.

The request carries `trace_ref=decision_trace_ref`. The Task Manager input
adapter uses that value for its candidate trace, with its existing generated
trace as the compatibility fallback when callers do not provide one. The
adapter's trace candidate is validated by both the object-compatible and
mapping-compatible forms of the existing Task Manager input contract.

Finding recorded during terminal verification: the Task Manager adapter sent
a mapping to `validate_tm_input_contract`, whose trace/fact/risk reads used
`getattr` only. This made an existing mapping `trace_ref` appear absent and
caused `missing_trace`/non-admission. The compatibility correction is
mapping-aware field access; the trace requirement itself remains mandatory.
