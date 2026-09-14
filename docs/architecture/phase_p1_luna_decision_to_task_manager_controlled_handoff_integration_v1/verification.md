# Verification

The verifier reads the runner summary and fails closed unless exactly two
positive cases are present. It validates Decision selection and provenance,
Decision-to-Task ownership, Task Manager admission, controlled Task state,
Task trace, and source Decision linkage.

It separately checks that the negative fixture is rejected without Task
Manager invocation and that all runtime side-effect flags remain false.

The negative result is derived from the actual rejected handoff, canonical
rejection reason, absent Task Manager invocation, and absent admitted handoff;
it is not a forced boolean. The positive Task Manager result is accepted only
when the canonical input-adaptation and admission steps both report `ok` and
the resulting state is one of the existing controlled lifecycle states.

Compatibility finding resolved: `validate_tm_input_contract` was object-only
while its canonical caller supplied a mapping. Its field reads are now
mapping-aware without removing the `missing_trace` guard.
