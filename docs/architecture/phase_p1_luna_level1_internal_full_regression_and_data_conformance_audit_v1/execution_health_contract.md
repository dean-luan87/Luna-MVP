# Execution Health Contract

Execution health records whether each declared current runner/verifier path
was available, executed in order, and returned its own expected result. Each
matrix entry records priority, dependency, arguments, output, archive-writing
behavior, and rerun safety.

The audit distinguishes `PASS`, `FAIL`, `WARNING`, and `BLOCKED`. A missing or
unreadable P0 output is a BLOCKER. A missing P1 output is a coverage finding,
not an implicit pass. Components without a dedicated verifier are explicitly
marked runner-only or contract-only.

Execution health does not infer runtime data correctness from an exit code.

Execution-health preflight has two independent gates: `compileall` checks
syntax/bytecode compilation, while `preflight_full_regression_v1` performs a
real import smoke of the canonical modules. Compileall PASS alone can never
establish execution-health PASS.

Before any state-producing Runner, the import preflight also records a
session baseline of observable output/archive file hashes, sizes, and
filesystem modification times. The read-only audit uses that baseline to
label artifacts `CURRENT_SESSION` or historical/unchanged. Without a valid
baseline, an existing PASS artifact is not evidence that the current
regression command ran and the audit fails closed.
