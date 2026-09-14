# Terminal evidence contract

Each required suite record contains:

- suite_id
- runner_ref
- verifier_ref
- expected_scenario_count
- observed_scenario_count
- all_cases_passed
- failed_case_ids
- blocker_count
- verification_status
- artifact_ref
- verified_by_user_terminal
- evidence_basis
- runner_stdout_observed
- coverage_mode
- subscope_refs

Missing records are `PENDING`; no field defaults to PASS.

The registered artifact is `terminal_evidence_registration_v1.json`. Intent and
Decision use verifier fixture coverage because their successful Runner runs
emit no stdout. Task uses `B3_SUBSCOPE` and has no standalone count.
