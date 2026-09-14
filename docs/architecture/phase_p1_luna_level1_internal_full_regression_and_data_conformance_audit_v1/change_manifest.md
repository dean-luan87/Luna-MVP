# Change Manifest

Created:

- `capabilities/evaluation/level1_cognitive_evaluation_run/audit_full_regression_v1.py`
- `capabilities/evaluation/level1_cognitive_evaluation_run/verify_full_regression_audit_v1.py`
- `capabilities/evaluation/level1_cognitive_evaluation_run/preflight_full_regression_v1.py`
- all documentation files in this phase directory.

Modified:

- the prior minimum-sufficient `full_regression_inventory.md` now points to
  this current inventory because its command list was stale.
- `runner_v1.py` and `fixture_v1.py` use per-execution Evaluation Run
  identities for rerun-safe synthetic archive writes.
- `run_controlled_replay_integration_v1.py` uses per-execution identity while
  preserving the historical fixed-identity archive record.
- the full-regression audit verifier requires session evidence.
- `audit_full_regression_v1.py` now gates archive cross-reference and Plane G
  checks by explicit component applicability and records the historical
  `CROSS-RUN-None` false positive as resolved.
- `audit_full_regression_v1.py` now gates phase presence by explicit
  `phase_required` applicability and records the Dataset Registry Stage 7
  false positive as resolved.
- The audit accepts the legacy `synthetic_candidate` mode only when it is
  sourced from the archive of an archive-required synthetic candidate; runtime
  components cannot use it as a substitute for a canonical execution mode.
- White-box foundation `verifier_v1.py` now evaluates the declared expected
  sufficiency outcome and explicit Current World expectation for guard
  scenarios; `fixtures_v1.py` declares the intentional missing Current World
  in `premature_sufficiency_guard`.
- `whitebox_foundation_regression_finding.md` records the Stage 1 MAJOR
  backward-compatibility finding and its pending terminal re-verification.

No cognition runtime, Dataset/Case contract, cognition semantics, Plane A/B/G
semantics, White-box V1 contract, archive writer, or archive record was
modified. Archive immutability was not weakened. The audit/preflight
utilities use only standard-library JSON/path inspection and session metadata.
