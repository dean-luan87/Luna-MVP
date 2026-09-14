# Scenario impact

## Direct controlled cases

The evaluation package covers legacy exact coverage, missing legacy coverage,
alternative basis A, alternative basis B, no basis covered, and multiple bases
covered. Multiple coverage still yields one semantic requirement and records
only actual matched coverage.

## Sandbox cases

- Scenario 12 now models one requirement, `exit_direction_known`, with signage
  and human-flow/environment as alternative satisfaction bases. Round 0 has no
  covered basis and retains the Need/exploration path. The simulated signage
  basis in Round 1 satisfies the same requirement; with no other requirement,
  the Need, Branch and Strategy for that gap are absent.
- Scenarios 02, 03 and 04 use one semantic exit-direction requirement with
  explicit alternative bases. Scenario 04 remains conflict-preserving; this
  phase does not resolve or fuse the conflicting sources.
- Scenario 10 remains valid: an unsatisfied requirement/Need may have zero
  governed acquisition strategies.
- Scenario 11 remains an irrelevant-change stability case; unrelated context
  does not reopen a satisfied requirement or regenerate its downstream gap.

The evaluation treats these as controlled semantic checks. It does not require
all scenarios to converge and does not add a hidden fallback strategy.
