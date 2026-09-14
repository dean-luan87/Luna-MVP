# Expected Outputs

Transient outputs remain below `_eval_out/`, including the seven current
foundation/replay summaries listed in `regression_inventory.md`.

Stage 0 additionally creates:

- `_eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/session_manifest_v1.json`

This is a session baseline, not a runtime result. It records only observable
pre-run file metadata and has no authority over cognition or the archive.

Durable replay records remain below:

`evaluation_archive/level1_cognitive_runs/`

The new audit produces:

- `_eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/full_regression_audit_report_v1.json`
- `_eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/full_regression_audit_report_v1.md`

The report contains the three layer counts, component/run/archive results,
cross references, governance and negative-guard findings, backward
compatibility status, severity counts, and `final_decision_candidate`.
It also contains `session_evidence`, distinguishing current-session artifacts
from historical or unchanged files. A missing or invalid session manifest is a
blocking condition for full-regression acceptance.

The report must additionally expose `operational_result` and
`cognitive_logic_result` as separate PASS/FAIL dimensions. The final decision
candidate cannot be `GO` unless both are `PASS` and the independent runtime and
artifact acceptance criteria are satisfied. Cognitive logic assertions follow
the shared [Luna Cognitive Logic Conformance Test
Contract](../luna_cognitive_logic_conformance_test_contract_v1.md).
