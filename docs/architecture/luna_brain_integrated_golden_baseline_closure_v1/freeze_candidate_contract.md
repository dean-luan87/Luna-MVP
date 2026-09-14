# Freeze candidate contract

States are `NOT_READY`, `READY_TO_FREEZE`, and
`FROZEN_BY_USER_DECISION`.

The integrated evaluator may produce only `READY_TO_FREEZE`. It never writes
the B5 manifest and never self-declares `LUNA_BRAIN_GOLDEN_BASELINE_V1_FROZEN`.
